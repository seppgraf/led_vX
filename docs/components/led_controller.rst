LED Controller Component
========================

.. comp:: LED Controller (Realtime)
   :id: COMP_LED_CTRL_RT
   :status: open
   :tags: component, led, cpp, realtime
   :links: ARCH_SW_RT_PROC, ARCH_SW_FRAME_ASM, COMP_SPI_DRV
   :language: C++17
   :layer: realtime

   The LED Controller component sits between the IPC layer and the SPI Driver.
   It owns the frame buffer, triggers the Frame Assembler, and drives the SPI
   Driver at the configured frame rate.

   **Responsibilities**

   * Maintain the canonical ``N × RGB`` colour frame buffer.
   * Accept updated frame data from the IPC Reader Thread (double-buffered).
   * At each tick, invoke the Frame Assembler to build the APA102 byte stream.
   * Delegate the byte stream to ``SpiDriver::write``.
   * Enforce timing: target frame interval = ``1 / fps`` seconds; compensate
     for variable ``SpiDriver::write`` latency using ``clock_nanosleep``.

   **File layout** (proposed)

   .. code-block:: text

      src/rt/
        led_controller.hpp
        led_controller.cpp
        frame_assembler.hpp
        frame_assembler.cpp

   **Public interface sketch**

   .. code-block:: cpp

      namespace led::rt {

      struct RgbPixel { std::uint8_t r, g, b; };

      class LedController {
      public:
          LedController(std::size_t n_leds,
                        SpiDriver&  spi,
                        unsigned    fps = 60);

          /// Called by IPC Reader Thread to swap in a new frame.
          void update_frame(std::span<const RgbPixel> pixels);

          /// Called by SPI Writer Thread; blocks for one frame interval.
          void tick();

      private:
          std::size_t              n_leds_;
          SpiDriver&               spi_;
          std::chrono::nanoseconds frame_period_;
          std::vector<RgbPixel>    front_buf_, back_buf_;
          std::atomic<bool>        frame_ready_{false};
          // ... synchronisation primitives
      };

      } // namespace led::rt

.. comp:: LED Controller (Python)
   :id: COMP_LED_CTRL_PY
   :status: open
   :tags: component, led, python, highlevel
   :links: ARCH_SW_PY_PROC, ARCH_SW_ANIM, IFACE_PY_API
   :language: Python
   :layer: highlevel

   The Python ``LedController`` class is the primary entry-point for all
   high-level LED control.

   **Responsibilities**

   * Manage connection to the shared-memory IPC segment.
   * Maintain an in-process RGB frame buffer (``numpy`` array for efficiency).
   * Provide ``fill``, ``set``, ``show`` primitives.
   * Delegate animation execution to the Animation Engine.
   * Handle graceful cleanup on ``__del__`` / context-manager ``__exit__``.

   **File layout** (proposed)

   .. code-block:: text

      src/py/
        led_ctrl/
          __init__.py
          controller.py     – LedController class
          colour.py         – Colour dataclass, colour helpers
          animations/
            __init__.py
            base.py         – Effect ABC
            solid.py
            rainbow.py
            pulse.py
            chase.py
          ipc.py            – IPC publisher (shared memory + semaphore)
          cli.py            – argparse CLI entry point

.. needtable::
   :filter: "component" in tags and "led" in tags
   :columns: id, title, status, links
   :style: table
