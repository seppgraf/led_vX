SPI Driver Component
====================

.. comp:: SPI Driver
   :id: COMP_SPI_DRV
   :status: open
   :tags: component, spi, cpp, realtime
   :links: SPEC_SW_SPI_DRIVER, SPEC_SW_SPI_CLK, IFACE_SPIDEV
   :language: C++17
   :layer: realtime

   The SPI Driver component encapsulates all interaction with the Linux
   ``spidev`` interface.  It provides a simple synchronous ``write`` API to
   the Frame Assembler and hides all ``ioctl`` details.

   **Responsibilities**

   * Open and configure ``/dev/spidev<bus>.<cs>`` at startup.
   * Set SPI mode (mode 0), bits-per-word (8), and clock frequency.
   * Provide a ``write(const std::span<const std::byte> data)`` method that
     blocks until the transfer is complete.
   * Close the file descriptor on destruction (RAII).

   **File layout** (proposed)

   .. code-block:: text

      src/rt/
        spi_driver.hpp   – public interface
        spi_driver.cpp   – implementation using spidev ioctls

   **Public interface sketch**

   .. code-block:: cpp

      namespace led::rt {

      struct SpiConfig {
          std::string device;          // e.g. "/dev/spidev0.0"
          std::uint32_t speed_hz;      // e.g. 8'000'000
          std::uint8_t  mode;          // SPI mode (0–3)
          std::uint8_t  bits_per_word; // typically 8
      };

      class SpiDriver {
      public:
          explicit SpiDriver(SpiConfig cfg);
          ~SpiDriver();

          // Non-copyable, movable
          SpiDriver(const SpiDriver&) = delete;
          SpiDriver& operator=(const SpiDriver&) = delete;

          /// Blocking full-duplex write. Returns after transfer completes.
          void write(std::span<const std::byte> data);

      private:
          int fd_{-1};
          SpiConfig cfg_;
      };

      } // namespace led::rt

   **Error handling**

   All ``ioctl`` failures throw ``std::system_error`` with the relevant
   ``errno``.

.. needtable::
   :filter: "component" in tags and "spi" in tags
   :columns: id, title, status, links
   :style: table
