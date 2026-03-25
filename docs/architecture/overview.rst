Architecture Overview
=====================

The LED Stripe Controller is a two-layer system running on a Raspberry Pi
under Linux.  A thin C++17 *realtime layer* handles all time-critical SPI
transactions, while a Python *high-level layer* provides pattern generation,
animation sequencing, and operator control.

.. arch:: System Context
   :id: ARCH_CONTEXT
   :status: open
   :tags: architecture, context
   :links: REQ_SYS_OS, REQ_SYS_HW

   The system operates as a single Linux process pair:

   * **led-rt** – a C++17 daemon that owns the ``/dev/spidev`` file descriptor
     and drives the LED stripe.
   * **led-ctrl** – a Python process (or library) that publishes LED colour
     frames to the realtime daemon through shared memory.

   An operator interacts exclusively with the Python layer.

.. arch:: Layered Architecture
   :id: ARCH_LAYERS
   :status: open
   :tags: architecture, layers
   :links: REQ_SYS_RT, REQ_SYS_HL

   The system is organised into three layers:

   1. **Hardware Abstraction Layer (HAL)** – Linux ``spidev`` kernel driver plus
      Raspberry Pi GPIO.
   2. **Realtime Layer (RTL)** – C++17 daemon; SPI frame assembly, scheduling,
      shutdown handling.
   3. **High-Level Layer (HLL)** – Python; colour management, animations, IPC
      publisher.

   ::

      ┌──────────────────────────────────────┐
      │       High-Level Layer (Python)      │
      │  Animation Engine │ Python API / CLI │
      └──────────────┬───────────────────────┘
                     │ shared memory + semaphore
      ┌──────────────▼───────────────────────┐
      │     Realtime Layer (C++17 daemon)    │
      │  Frame Assembler │ SPI Scheduler     │
      └──────────────┬───────────────────────┘
                     │ spidev ioctl
      ┌──────────────▼───────────────────────┐
      │   Hardware Abstraction Layer (Linux) │
      │         /dev/spidevX.Y               │
      └──────────────┬───────────────────────┘
                     │ SPI bus (MOSI/SCLK/CE)
      ┌──────────────▼───────────────────────┐
      │         LED Stripe (APA102)          │
      └──────────────────────────────────────┘

.. arch:: Deployment View
   :id: ARCH_DEPLOY
   :status: open
   :tags: architecture, deployment
   :links: REQ_SYS_HW, REQ_SYS_OS

   Both processes run on the same Raspberry Pi node.  The realtime daemon is
   started as a ``systemd`` service with elevated scheduling priority; the
   Python controller is started either as a second ``systemd`` service or
   interactively by an operator.

.. needtable::
   :filter: "architecture" in tags
   :columns: id, title, status
   :style: table
