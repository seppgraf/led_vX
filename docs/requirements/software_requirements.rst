Software Requirements
=====================

This section specifies software-level requirements derived from the system
requirements. Each requirement references its parent system requirement.

.. spec:: Linux Kernel SPI Driver Usage
   :id: SPEC_SW_SPI_DRIVER
   :status: open
   :tags: software, spi, linux
   :links: REQ_SYS_SPI
   :language: C++17
   :layer: realtime

   The realtime layer shall use the Linux ``spidev`` kernel interface to access
   the SPI bus (``/dev/spidevX.Y``).

.. spec:: SPI Clock Frequency
   :id: SPEC_SW_SPI_CLK
   :status: open
   :tags: software, spi
   :links: REQ_SYS_SPI
   :language: C++17
   :layer: realtime

   The SPI clock frequency shall be configurable and shall default to 8 MHz to
   satisfy the timing requirements of common LED stripe ICs (e.g. APA102).

.. spec:: Realtime Thread Priority
   :id: SPEC_SW_RT_PRIO
   :status: open
   :tags: software, realtime, linux
   :links: REQ_SYS_RT
   :language: C++17
   :layer: realtime

   The SPI transmission thread shall run with ``SCHED_FIFO`` scheduling policy
   and a priority of 80 (out of 99) to meet the 100 µs jitter requirement.

.. spec:: C++17 Realtime Layer
   :id: SPEC_SW_CPP_RT
   :status: open
   :tags: software, realtime, cpp
   :links: REQ_SYS_RT
   :language: C++17
   :layer: realtime

   All time-critical operations (SPI frame assembly, DMA-burst scheduling,
   colour-space conversion) shall be implemented in C++17.

.. spec:: Python High-Level API
   :id: SPEC_SW_PY_API
   :status: open
   :tags: software, python, api
   :links: REQ_SYS_HL
   :language: Python
   :layer: highlevel

   High-level control logic (animation sequencing, colour management, user
   interface) shall be implemented in Python (≥ 3.10).

.. spec:: IPC Between Python and C++ Layer
   :id: SPEC_SW_IPC
   :status: open
   :tags: software, ipc
   :links: REQ_SYS_HL, REQ_SYS_RT

   The Python layer shall communicate with the C++17 realtime layer through a
   shared-memory ring-buffer and a POSIX named semaphore to minimise latency.

.. spec:: LED Frame Format
   :id: SPEC_SW_FRAME
   :status: open
   :tags: software, spi, led
   :links: REQ_SYS_SPI
   :language: C++17
   :layer: realtime

   The C++17 layer shall assemble SPI frames according to the APA102 protocol:
   start frame (32 zero bits), one 32-bit LED word per LED, and an end frame
   (ceiling(N/2) one-bits for N LEDs).

.. spec:: Graceful Shutdown Handler
   :id: SPEC_SW_SHUTDOWN
   :status: open
   :tags: software, safety
   :links: REQ_SYS_SAFE
   :language: C++17
   :layer: realtime

   The realtime layer shall register a handler for ``SIGTERM`` and ``SIGINT``
   that sends an all-zeros SPI frame before terminating the process.

.. needtable::
   :filter: "software" in tags
   :columns: id, title, status, links
   :style: table
