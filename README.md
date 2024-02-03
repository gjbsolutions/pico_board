# pico_board

Βασική πλακετούλα με pi pico η οποία έχει μια oled screen, δυο κουμπάκια για input, μπαταρία 18650 για παροχή ισχύος και κύκλωμα φόρτισης μπαταρίας.

- Ο διαιρέτης τάσης χρησιμοποιείται για μέτρηση της τάσης μπαταρίας. Μπορεί να έχει δύο όμοιες αντιστάσεις >10kΩ.
- Υπάρχουν δύο έξοδοι για περιφερειακές συσκευές. Μια στην SPI και η άλλη για I2C ή UART


![Pico_Board](pico_board.jpg)

Το κύκλωμα τροφοδοσίας που αποτελείται από μια μπαταρία 18650 και ένα κύκλωμα φόρτισης τέτοιας μπαταρίας 3.7V από το aliexpress

![Pico_Board](pico_board_back.jpg)

Η μπροστινή όψη του project με συνδεδεμένο ένα RF module επικοινωνίας CC1101 στην SPI θύρα του pico

![Pico_Board](pico_board_front.jpg)

**Παράδειγμα Μετάδοσης - Λήψης με CC1101**

Στην περίπτωση που θέλετε να χρησιμοποιήσετε το RF module CC1101, υπάρχουν δύο demo (ένα για λήψη Rx και ένα για μετάδοση Tx) στον κώδικα τα οποία λειτουργούν αλλά δεν έχουν όλες τις λειτουργίες που υπάρχουν σε βιβλιοθήκες για άλλα microcontroller. Στο pico βρήκα μόνο βιβλιοθήκη cc1101 για circuitpython και από εκεί προσπάθησα να προσαρμόσω κώδικα. Για τα υπόλοιπα RF modules (nrf24, Lora) βρίσκεις εύκολα πλήρεις βιβλιοθήκες στο pico. Η συνδεσμολογία στο pico φαίνεται στο σχήμα

![cc1101](pico_board_cc1101.jpg)

