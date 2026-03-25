Python API Component
====================

.. comp:: Python Animation Engine
   :id: COMP_PY_ANIM
   :status: open
   :tags: component, python, animation, highlevel
   :links: ARCH_SW_ANIM, COMP_LED_CTRL_PY
   :language: Python
   :layer: highlevel

   The Animation Engine schedules and composites *Effect* objects onto the
   frame buffer.

   **Responsibilities**

   * Maintain a list of active ``Effect`` instances.
   * Drive a render loop at the configured frame rate using ``threading.Event``
     for precise timing.
   * Call ``Effect.render(t: float, buf: np.ndarray)`` for each active effect.
   * Composite results (alpha-blend or last-writer-wins) into the final buffer.
   * Forward the composited frame to ``LedController.show()``.

   **Effect ABC**

   .. code-block:: python

      from abc import ABC, abstractmethod
      import numpy as np

      class Effect(ABC):
          """Base class for all LED animation effects."""

          @abstractmethod
          def render(self, t: float, buf: np.ndarray) -> None:
              """
              Render the effect into *buf* at time *t* (seconds since start).

              :param t:   Time in seconds since the effect started.
              :param buf: Shape (N, 3) uint8 array; columns are R, G, B.
              """

.. comp:: IPC Publisher
   :id: COMP_IPC_PUB
   :status: open
   :tags: component, python, ipc
   :links: SPEC_SW_IPC, ARCH_SW_IPC_PUB, IFACE_SHM_IPC
   :language: Python
   :layer: highlevel

   The IPC Publisher serialises the Python frame buffer and delivers it to the
   C++17 realtime layer via POSIX shared memory.

   **Responsibilities**

   * On ``open()``: create or attach to the shared-memory segment
     (``/led_frame_buffer``) and the semaphore (``/led_frame_sem``).
   * On ``publish(frame: np.ndarray)``: write the frame to the inactive buffer
     slot, increment the write index atomically, and post the semaphore.
   * On ``close()``: detach from shared memory; optionally unlink if owner.

   **Python sketch**

   .. code-block:: python

      import mmap, posix_ipc, ctypes, numpy as np

      class IpcPublisher:
          def __init__(self, n_leds: int, name: str = "/led_frame_buffer"):
              self.n_leds = n_leds
              self._shm   = posix_ipc.SharedMemory(name, flags=posix_ipc.O_CREAT,
                                                   size=self._shm_size())
              self._sem   = posix_ipc.Semaphore("/led_frame_sem",
                                                flags=posix_ipc.O_CREAT)
              self._map   = mmap.mmap(self._shm.fd, self._shm_size())

          def publish(self, frame: np.ndarray) -> None:
              # Write to inactive buffer, swap index, post semaphore
              ...

          def _shm_size(self) -> int:
              return 16 + 2 * (4 * self.n_leds)

.. comp:: CLI Entry Point
   :id: COMP_CLI
   :status: open
   :tags: component, python, cli
   :links: IFACE_CLI, COMP_LED_CTRL_PY
   :language: Python
   :layer: highlevel

   The ``led-ctrl`` CLI is implemented as an ``argparse`` application in
   ``src/py/led_ctrl/cli.py``.

   **Subcommands**

   ==================  ================================================
   Subcommand          Description
   ==================  ================================================
   ``fill COLOUR``     Fill all LEDs with a hex colour (e.g. ``ff0000``).
   ``off``             Turn all LEDs off.
   ``animate NAME``    Run a named built-in animation.
   ``list-effects``    Print available effect names.
   ==================  ================================================

   **Example**

   .. code-block:: shell

      led-ctrl fill ff8000          # orange
      led-ctrl animate rainbow --fps 30 --duration 60
      led-ctrl off

.. needtable::
   :filter: "component" in tags and "python" in tags
   :columns: id, title, status, links
   :style: table
