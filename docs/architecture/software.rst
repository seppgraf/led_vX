Software Architecture
=====================

The software is split into two cooperating processes: the C++17 realtime
daemon (``led-rt``) and the Python high-level controller (``led-ctrl``).

Realtime Layer (C++17)
----------------------

.. arch:: Realtime Daemon Process
   :id: ARCH_SW_RT_PROC
   :status: open
   :tags: architecture, software, realtime, cpp
   :links: SPEC_SW_CPP_RT, SPEC_SW_RT_PRIO

   ``led-rt`` is a single C++17 process started by ``systemd`` with
   ``AmbientCapabilities=CAP_SYS_NICE`` to allow ``SCHED_FIFO`` scheduling.
   The process contains three internal threads:

   1. **SPI Writer Thread** – ``SCHED_FIFO`` priority 80; dequeues colour
      frames and transmits them via ``spidev`` ``ioctl(SPI_IOC_MESSAGE)``.
   2. **IPC Reader Thread** – ``SCHED_FIFO`` priority 70; receives frames from
      the Python layer via the shared-memory ring-buffer.
   3. **Watchdog Thread** – normal priority; monitors heartbeat from the
      Python layer and triggers a safe-state frame if the heartbeat is missed.

.. arch:: SPI Frame Assembler
   :id: ARCH_SW_FRAME_ASM
   :status: open
   :tags: architecture, software, realtime, spi
   :links: SPEC_SW_FRAME, SPEC_SW_SPI_DRIVER, SPEC_SW_SPI_CLK

   The Frame Assembler converts an array of RGB colour values (received from
   the IPC ring-buffer) into a raw APA102 SPI byte stream:

   * **Start frame**: 4 bytes of ``0x00``.
   * **LED frames**: ``N × 4`` bytes – ``[0xFF, B, G, R]`` per LED.
   * **End frame**: ``⌈N / 2⌉`` bytes of ``0xFF``.

   Colour-space conversion (linear RGB → gamma-corrected LED PWM) is applied
   in this stage using a pre-computed lookup table.

.. arch:: Shutdown Handler
   :id: ARCH_SW_SHUTDOWN
   :status: open
   :tags: architecture, software, realtime, safety
   :links: SPEC_SW_SHUTDOWN, REQ_SYS_SAFE

   A ``sigaction`` handler registered for ``SIGTERM`` and ``SIGINT`` sets an
   atomic flag that causes the SPI Writer Thread to transmit one all-zeros
   frame and then exit cleanly.

High-Level Layer (Python)
--------------------------

.. arch:: Python Controller Process
   :id: ARCH_SW_PY_PROC
   :status: open
   :tags: architecture, software, python, highlevel
   :links: SPEC_SW_PY_API, SPEC_SW_IPC

   ``led-ctrl`` is a Python (≥ 3.10) process or importable library that
   provides:

   * A :class:`LedController` class as the primary public API.
   * An animation engine that calls :meth:`LedController.show` at a configurable
     frame rate (default 60 fps).
   * A CLI entry point (``led-ctrl show``, ``led-ctrl animate``, etc.) built
     with ``argparse``.

.. arch:: Animation Engine
   :id: ARCH_SW_ANIM
   :status: open
   :tags: architecture, software, python, highlevel
   :links: ARCH_SW_PY_PROC

   The Animation Engine maintains a list of *Effect* objects.  On each tick it
   calls ``Effect.render(t, frame_buffer)`` for every active effect, composites
   the results, and forwards the final frame buffer to the IPC publisher.

   Built-in effects include:

   * ``SolidColour`` – fills all LEDs with one colour.
   * ``Rainbow`` – cycles through the HSV colour wheel.
   * ``Pulse`` – sinusoidal brightness modulation.
   * ``Chase`` – travelling dot / comet.

.. arch:: IPC Publisher
   :id: ARCH_SW_IPC_PUB
   :status: open
   :tags: architecture, software, python, ipc
   :links: SPEC_SW_IPC

   The IPC Publisher writes serialised RGB frames into a POSIX shared-memory
   segment and posts a named semaphore to wake the C++17 IPC Reader Thread.
   The shared-memory segment size is ``4 × N + 64`` bytes (N = LED count),
   providing a double-buffering scheme to avoid tearing.

Inter-Process Communication
----------------------------

.. arch:: Shared Memory Ring-Buffer
   :id: ARCH_SW_SHM
   :status: open
   :tags: architecture, software, ipc
   :links: SPEC_SW_IPC, ARCH_SW_IPC_PUB, ARCH_SW_RT_PROC

   The shared-memory segment is mapped by both ``led-rt`` and ``led-ctrl``.
   The layout is:

   ========  =========  ================================================
   Offset    Size       Description
   ========  =========  ================================================
   0         4 B        Magic number (``0x4C454400``)
   4         4 B        LED count (N)
   8         4 B        Write index (atomic)
   12        4 B        Read index (atomic)
   16        4×N B      Frame buffer A (RGB, 1 byte per channel)
   16+4N     4×N B      Frame buffer B (RGB, 1 byte per channel)
   ========  =========  ================================================

.. needtable::
   :filter: "software" in tags and "architecture" in tags
   :columns: id, title, status, links
   :style: table
