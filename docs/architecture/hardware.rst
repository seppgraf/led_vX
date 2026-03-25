Hardware Architecture
=====================

This section describes the physical hardware involved in the LED Stripe
Controller system.

.. arch:: Raspberry Pi Processing Unit
   :id: ARCH_HW_RPI
   :status: open
   :tags: architecture, hardware
   :links: REQ_SYS_HW

   The Raspberry Pi (generation 3 or newer) provides:

   * A quad-core ARM Cortex-A53/A72 processor running Linux.
   * A hardware SPI controller accessible via ``/dev/spidev0.0`` (and
     ``/dev/spidev0.1`` for a second chip-select).
   * 3.3 V logic levels on all SPI pins.

   The SPI peripheral supports full-duplex operation; for LED stripe use only
   MOSI (GPIO 10) and SCLK (GPIO 11) are required.  CE0 (GPIO 8) is used as
   chip-select.

.. arch:: SPI Bus
   :id: ARCH_HW_SPI
   :status: open
   :tags: architecture, hardware, spi
   :links: REQ_SYS_SPI, ARCH_HW_RPI

   The SPI bus connects the Raspberry Pi to the first LED in the stripe.

   ============  ===========  ===========
   Signal        RPi Pin      LED Stripe
   ============  ===========  ===========
   MOSI          GPIO 10      Data In (DI)
   SCLK          GPIO 11      Clock In (CI)
   GND           Pin 6 / 9    GND
   ============  ===========  ===========

   A level shifter (3.3 V → 5 V) is recommended between the Raspberry Pi and
   the LED stripe to ensure reliable data reception.

.. arch:: LED Stripe
   :id: ARCH_HW_LED
   :status: open
   :tags: architecture, hardware, led
   :links: REQ_SYS_SPI, ARCH_HW_SPI

   The LED stripe consists of APA102 (or compatible) addressable RGB LEDs
   daisy-chained on a shared SPI bus.  Each LED contains an integrated driver
   IC that latches its colour word on the rising edge of the clock.

   Key electrical parameters:

   * Supply voltage: 5 V DC.
   * Current per LED (full white): ≈ 60 mA.
   * Maximum SPI clock: 20 MHz (datasheet); 8 MHz used for margin.

.. arch:: Power Supply
   :id: ARCH_HW_POWER
   :status: open
   :tags: architecture, hardware
   :links: ARCH_HW_LED

   A dedicated 5 V power supply with sufficient current capacity shall power
   the LED stripe directly (not through the Raspberry Pi 5 V rail).  The
   Raspberry Pi and LED stripe share a common GND reference.

.. needtable::
   :filter: "hardware" in tags
   :columns: id, title, status
   :style: table
