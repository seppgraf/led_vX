Traceability Matrix
===================

This page provides full cross-referencing between system requirements,
software specifications, architecture elements, components, and interfaces.

All Needs
---------

.. needtable::
   :columns: id, type, title, status, links
   :style: table

Requirement → Specification Coverage
-------------------------------------

.. needflow::
   :filter: type in ["req", "spec"]
   :show_link_names:

Specification → Architecture Coverage
--------------------------------------

.. needflow::
   :filter: type in ["spec", "arch"]
   :show_link_names:

Architecture → Component Coverage
-----------------------------------

.. needflow::
   :filter: type in ["arch", "comp", "iface"]
   :show_link_names:
