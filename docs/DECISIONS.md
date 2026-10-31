# Design Decisions

This file records decisions that should not be rediscovered from scratch in every new session.

## D001 — Final compute board
**Decision:** Raspberry Pi 3 Model A+ is the final embedded compute target.

**Reason:** It is smaller than the Pi 5, has already run the calculator software successfully, and fits the TI-83 Plus enclosure better.

**Status:** Locked unless a future hardware revision explicitly replaces it.

---

## D002 — Development board
**Decision:** Raspberry Pi 5 remains the development/debug board.

**Reason:** It is already configured and was used to prove the camera/software stack.

---

## D003 — Donor enclosure
**Decision:** Use a TI-83 Plus donor shell rather than the thinner Casio fx-991CW shell.

**Reason:** The TI-83 Plus provides significantly more internal volume and a reusable keypad/membrane structure.

---

## D004 — Display
**Decision:** Keep the Waveshare 2.8-inch 480x640 portrait touchscreen.

**Reason:** The UI is already optimized and validated on this display. The LCD/touch assembly survived separation and reconnection from its controller PCB.

---

## D005 — Camera
**Decision:** Keep Raspberry Pi Camera Module 3 Wide NoIR and connect it directly to the Pi over CSI.

**Reason:** Camera solving is already tested with this hardware.

**PCB implication:** Rev 1 should provide ribbon clearance rather than rerouting CSI signals through the custom PCB.

---

## D006 — Keypad architecture
**Decision:** Final design should move away from the bulky ESP32-S3 development board and toward a custom PCB that integrates keypad contacts and an ESP32-S3 module.

**Reason:** The dev board works electrically but does not fit cleanly in the enclosure.

---

## D007 — Original TI keypad
**Decision:** Reuse the original TI plastic keys and rubber membrane where practical.

**Reason:** This preserves calculator feel and avoids fabricating dozens of custom mechanical switches.

**PCB implication:** Custom PCB contact geometry must align precisely with the conductive rubber contacts.

---

## D008 — Current logical keypad
**Decision:** Preserve the current 6x6 / 36-command logical map until the final keypad redesign intentionally changes it.

**Reason:** The firmware and Raspberry Pi application already support and test this mapping.

---

## D009 — Power source
**Decision:** Final current direction is the original 4xAAA rear battery compartment.

**Reason:** It preserves the TI-83 exterior and avoids fitting a thick lithium pack inside the shell.

**Important constraint:** AAA cells must never be wired directly to the Pi. A regulated 5 V supply is required.

---

## D010 — Power topology
**Decision:** Use a buck-boost 5 V power stage for the 4xAAA system.

**Reason:** Four AAA cells may be above or below 5 V depending on cell chemistry and discharge state.

**Open risk:** AAA cells may not provide enough peak current or acceptable runtime for Pi + display + camera + Wi-Fi. This must be validated experimentally before the power architecture is considered final.

---

## D011 — First custom PCB power design
**Decision:** Prefer a proven high-current buck-boost module mounted to PCB Rev 1 rather than immediately designing a multi-amp switching converter from scratch.

**Reason:** Reduces the risk of combining a first mechanical/keypad PCB revision with a difficult power-electronics layout on the same unproven board.

**Future:** Rev 2 may integrate the regulator circuitry directly after the mechanical/electrical architecture is proven.

---

## D012 — Pi/ESP32 communication
**Decision:** UART is the preferred final internal transport, while maintaining the same simple `KEY:<name>` message protocol where practical.

**Reason:** It eliminates the bulky USB connection and preserves the existing event architecture.

**Status:** Preferred, not yet implemented.

---

## D013 — PCB fabrication workflow
**Decision:** Design in KiCad and fabricate through JLCPCB.

**Manufacturing output:** Gerbers + Excellon drill files. A PDF is for 1:1 fit checking, not the manufacturing source.

---

## D014 — Mechanical validation
**Decision:** Never order a custom keypad PCB without first printing the PCB layout at 100% / 1:1 scale and verifying the outline, holes, keypad contacts, and keep-outs against the real TI shell and membrane.

**Reason:** Mechanical alignment is a critical project risk.

---

## D015 — Course mode
**Decision:** Keep ECE 361 as an explicit CAMERA method mode backed by `ece361_method.txt`.

**Reason:** It must follow the course's taught notation and equation order rather than generic shortcuts.

---

## D016 — AI formatting stability
**Decision:** Do not casually rewrite the approved AI text-response format.

**Reason:** It was already tuned for the small display and tested by the user.

---

## D017 — Documentation as project memory
**Decision:** The Git repository, especially `AGENTS.md` and `docs/`, is the durable project memory for future Codex work.

**Reason:** Chat history is too long and too fragile to serve as the authoritative project specification.
