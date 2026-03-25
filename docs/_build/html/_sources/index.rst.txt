LED Stripe Controller – Architecture Documentation
==================================================

This document describes the architecture of the LED Stripe Controller system.
The system controls an LED stripe via SPI from a Raspberry Pi running Linux.
Real-time control is implemented in C++17; high-level orchestration is done in
Python.

.. toctree::
   :maxdepth: 2
   :caption: Requirements

   requirements/system_requirements
   requirements/software_requirements

.. toctree::
   :maxdepth: 2
   :caption: Architecture

   architecture/overview
   architecture/hardware
   architecture/software
   architecture/interfaces

.. toctree::
   :maxdepth: 2
   :caption: Components

   components/spi_driver
   components/led_controller
   components/python_api

.. toctree::
   :maxdepth: 1
   :caption: Traceability

   traceability

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`search`
