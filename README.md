# pico_board

Βασική πλακετούλα με pi pico η οποία έχει μια oled screen, δυο κουμπάκια για input, μπαταρία 18650 για παροχή ισχύος και κύκλωμα φόρτισης μπαταρίας.

- Ο διαιρέτης τάσης χρησιμοποιείται για μέτρηση της τάσης μπαταρίας. Μπορεί να έχει δύο όμοιες αντιστάσεις >10kΩ.
- Υπάρχουν δύο έξοδοι για περιφερειακές συσκευές. Μια στην SPI και η άλλη για I2C ή UART


![Pico_Board](pico_board.jpg)

Το κύκλωμα τροφοδοσίας που αποτελείται από μια μπαταρία 18650 και ένα κύκλωμα φόρτισης τέτοιας μπαταρίας 3.7V από το aliexpress

![Pico_Board](pico_board_photo.jpg)

**Παράδειγμα Μετάδοσης - Λήψης με CC1101**

Στην περίπτωση που θέλετε να χρησιμοποιήσετε το RF module CC1101, υπάρχουν δύο demo (ένα για λήψη Rx και ένα για μετάδοση Tx) στον κώδικα τα οποία λειτουργούν αλλά δεν έχουν όλες τις λειτουργίες που υπάρχουν σε βιβλιοθήκες για άλλα microcontroller. Στο pico βρήκα μόνο βιβλιοθήκη cc1101 για circuitpython και από εκεί προσπάθησα να προσαρμόσω κώδικα. Για τα υπόλοιπα RF modules (nrf24, Lora) βρίσκεις εύκολα πλήρεις βιβλιοθήκες στο pico. Η συνδεσμολογία στο pico φαίνεται στο σχήμα

![cc1101](pico_board_cc1101.jpg)

**Παράδειγμα Scanner με NRF24**

Η συνδεσμολογία Pin του NRF24 στο board είναι απολύτως όμοια με προηγουμένως. Το demo του rf24 στα αρχεία κάνει χρήση της βιβλιοθήκης nrf24l01.py. Εκτελεί σκανάρισμα στις συχνότητες 2400 - 2525MHz και δείχνει αριθμητικά την δραστηριότητα σε κάθε κομματάκι 5MHz του φάσματος στην oled οθόνη.

![cc1101](pico_board_nrf24.jpg)

**Παράδειγμα Μετάδοσης - Λήψης με HC-12**

![Pico_Board](HC12.jpg)

Προστέθηκε στα παραδείγματα η λήψη και μετάδοση με HC-12. Σε περίπτωση που θελήσετε να αλλάξετε τις παραμέτρους του HC-12 διαβάστε για τις AT εντολές στο datasheet που θα βρείτε στο ίντερνετ και θέστε το SET PIN (LOW) με κάποιο από τα GP pins του pico.

**Παράδειγμα για λήψη gps με το module E108 της EBYTE**

![Pico_Board](GPS.jpg)

To Rx(5) θα συνδεθεί στο GP0 pin του pico και το Tx(4) θα συνδεθεί στο pin GP1 του pico.

**Παράδειγμα για μετάδοση μόνο με το Pico**

Ο μικροελεγκτής από μόνος του μπορεί να μεταδώσει σήμα με διαμόρφωση OOK. Η λογική είναι να δημιουργείς παλμούς μεγάλης συχνότητας σε ένα από τα Pin και να τους ανοιγοκλείνεις ανάλογα με τι τιμή bit (1 ή 0) θέλεις να στείλεις. Ένα μικρό συρματάκι μπορεί να παίξει τον ρόλο κεραίας. Η ισχύ δεν είναι ιδιαίτερα μεγάλη (στην καλύτερη περίπτωση μερικά mW) αλλά καλό είναι να ληφθεί μέριμνα ώστε το σήμα να μην δημιουργήσει προβλήματα σε τρίτους. Πχ βάλτε ένα μικρό σε μήκος συρματάκι ως κεραία και όχι το σωστό μήκος για την συγκεκριμένη συχνότητα ώστε το σήμα να είναι υπερβολικά εξασθενημένο. 


**Παράδειγμα κρυπτογράφησης**

Συχνά υπάρχει ανάγκη κρυπτογράφησης των μυνημάτων, προστέθηκε παράδειγμα κρυπτογράφησης AES

![Pico_Board](encrypt.jpg)

**Παράδειγμα accelerometer MPU6050**

![Pico_Board](mpu6050.jpg)

**Παράδειγμα LORA Ebyte E220**

Αυτό το παράδειγμα καλό είναι να εκτελεστεί σε ένα breadboard γιατί απαιτούνται επιπλέον αντιστάσεις 4.7kΩ

Οι βιβλιοθήκες είναι τα αρχεία
* lora_e220.py
* lora_e220_constants.py
* lora_e220_operation_constant.py

Το demo_E220.py χρησιμοποιεί το mode που δεν χρειάζεται κανένα σετάρισμα, ο πομπός και ο δέκτης δουλεύουν με τον ίδιο κώδικα

Το demo_E220_RX.py έχει στα comments κώδικα που χρειάζεται για να σετάρεις τα modules στις ιδιότητες που θέλεις και δουλεύει με το demo_E220_TX.py ως πομπό

![Pico_Board](e220.jpg)

**PCB board**

Προστέθηκαν τα Gerber Files της πλακέτας

![Pico_Board](pico_pcb.jpg)



