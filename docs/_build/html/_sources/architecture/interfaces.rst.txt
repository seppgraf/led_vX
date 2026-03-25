Interfaces
==========

This section describes all externally visible interfaces of the LED Stripe
Controller system.

.. iface:: spidev Kernel Interface
   :id: IFACE_SPIDEV
   :status: open
   :tags: interface, spi, linux, kernel
   :links: SPEC_SW_SPI_DRIVER, ARCH_SW_FRAME_ASM

   The C++17 realtime layer communicates with the Linux SPI subsystem through
   the ``spidev`` character device.

   * **File**: ``/dev/spidev<bus>.<cs>`` (default ``/dev/spidev0.0``).
   * **Open flags**: ``O_RDWR``.
   * **Control**: ``ioctl(fd, SPI_IOC_WR_MODE, &mode)`` to set mode 0 (CPOL=0,
     CPHA=0); ``ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed)`` to set clock.
   * **Transmission**: ``ioctl(fd, SPI_IOC_MESSAGE(1), &xfer)`` with a
     ``struct spi_ioc_transfer`` describing a single full-duplex transfer (only
     MOSI data is relevant for LED stripes).

.. iface:: Shared Memory IPC Interface
   :id: IFACE_SHM_IPC
   :status: open
   :tags: interface, ipc, sharedmemory
   :links: SPEC_SW_IPC, ARCH_SW_SHM

   The shared-memory segment is the primary IPC channel between the Python
   high-level layer and the C++17 realtime layer.

   * **Name**: ``/led_frame_buffer`` (POSIX ``shm_open``).
   * **Semaphore**: ``/led_frame_sem`` (POSIX ``sem_open``).
   * **Protocol**: The Python publisher writes a complete RGB frame into the
     inactive buffer, increments the write index atomically, then posts the
     semaphore.  The C++ IPC Reader Thread wakes on the semaphore, swaps the
     active buffer index, and notifies the SPI Writer Thread.

.. iface:: Python LedController API
   :id: IFACE_PY_API
   :status: open
   :tags: interface, python, api
   :links: SPEC_SW_PY_API, ARCH_SW_PY_PROC

   The primary Python API exposed to operators and application code:

   .. code-block:: python

      from led_ctrl import LedController, Colour

      ctrl = LedController(n_leds=144, spi_bus=0, spi_cs=0)
      ctrl.open()

      # Set all LEDs to red
      ctrl.fill(Colour(r=255, g=0, b=0))
      ctrl.show()

      # Run a built-in animation
      ctrl.animate("rainbow", fps=60, duration_s=10)

      ctrl.close()

   Key methods:

   =====================  ====================================================
   Method                 Description
   =====================  ====================================================
   ``open()``             Opens the SPI device and shared-memory segment.
   ``close()``            Sends an all-off frame and releases resources.
   ``fill(colour)``       Fills all LEDs with a single :class:`Colour`.
   ``set(i, colour)``     Sets the colour of LED at index *i*.
   ``show()``             Pushes the current frame buffer to the realtime layer.
   ``animate(name)``      Starts a named built-in animation in a background
                          thread.
   =====================  ====================================================

.. iface:: Command-Line Interface
   :id: IFACE_CLI
   :status: open
   :tags: interface, python, cli
   :links: ARCH_SW_PY_PROC

   The ``led-ctrl`` command-line tool provides operator access:

   .. code-block:: shell

      # Turn all LEDs red
      led-ctrl fill --colour ff0000

      # Run rainbow animation for 30 seconds
      led-ctrl animate rainbow --duration 30 --fps 60

      # Turn all LEDs off
      led-ctrl off

.. iface:: systemd Service Interface
   :id: IFACE_SYSTEMD
   :status: open
   :tags: interface, linux, systemd, deployment
   :links: ARCH_SW_RT_PROC, ARCH_DEPLOY

   The realtime daemon is managed as a ``systemd`` service unit
   (``led-rt.service``).  Key unit properties:

   * ``Type=exec``
   * ``AmbientCapabilities=CAP_SYS_NICE``
   * ``Restart=on-failure``
   * ``RestartSec=1s``

.. needtable::
   :filter: "interface" in tags
   :columns: id, title, status, links
   :style: table
