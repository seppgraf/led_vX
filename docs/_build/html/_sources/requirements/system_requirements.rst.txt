System Requirements
===================

This section captures the top-level system requirements for the LED Stripe
Controller. All requirements are traceable to software specifications and
architecture elements.

.. req:: Operating System
   :id: REQ_SYS_OS
   :status: open
   :tags: system, platform

   The system shall run on a Linux-based operating system.

.. req:: Target Hardware Platform
   :id: REQ_SYS_HW
   :status: open
   :tags: system, hardware
   :rationale: Raspberry Pi provides GPIO, SPI bus, and sufficient CPU power for
      the intended use-case at low cost.

   The system shall execute on a Raspberry Pi (generation 3 or newer).

.. req:: LED Stripe Communication Protocol
   :id: REQ_SYS_SPI
   :status: open
   :tags: system, hardware, spi

   The LED stripe shall be controlled via the SPI bus exposed by the Raspberry Pi.

.. req:: Realtime Control
   :id: REQ_SYS_RT
   :status: open
   :tags: system, realtime

   The system shall guarantee that SPI frame transmission jitter does not exceed
   100 µs.

.. req:: High-Level Control Interface
   :id: REQ_SYS_HL
   :status: open
   :tags: system, api

   The system shall expose a high-level API that allows an operator to program
   LED animations and colour patterns without knowledge of the SPI protocol.

.. req:: Safety Shutdown
   :id: REQ_SYS_SAFE
   :status: open
   :tags: system, safety

   In the event of a software fault or OS signal, the system shall transition
   all LEDs to the *off* state within 500 ms.

.. needtable::
   :filter: "system" in tags
   :columns: id, title, status
   :style: table
