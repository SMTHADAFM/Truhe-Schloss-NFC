# Bibliotheken für den Kartenleser
import RPi.GPIO as GPIO
import MFRC522
import signal

# Websocket Bibliotheken
import asyncio
import websockets

##
# Start der Anwendung und Vorbereitung aller benötigten Funktionalitäten
##

websocketServer = "ws://localhost:8000"  # Die Adresse der Truhe. localhost kann im Netzwerk durch die IP-Adresse ausgetauscht werden

# Diese Variable steuert die Abfrage nach neuen RFID-Karten
continue_reading = True


# Beende das lesen vom NFC-Lesegerät
def end_read(signal, frame):
    global continue_reading
    print("Ende der Ausführung")
    continue_reading = False
    GPIO.cleanup()


# Warte auf Abbruch Befehl vom Betriebssystem
signal.signal(signal.SIGINT, end_read)

# Initailaisiere die Klasse MRFC522
MIFAREReader = MFRC522.MFRC522()


async def ReadFromCardreader():
    # Führe diese Schleife immer wieder aus, bis diese durch end_read() unterbrochen wird
    while continue_reading:

        # Lese die Daten einer Karte ein
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # wenn durch status eine AKrte gefunden wird, gebe dies aus
        if status == MIFAREReader.MI_OK:
            print("Karte erkannt")

        # Lese die Karte erneut und entnehme die uniqe id
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # wenn durch satus eine Karte erkannt wurde, fahre fort
        if status == MIFAREReader.MI_OK:
            # Gebe die uniqe id aus
            print("UID der Karte lautet: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))

            uidString = convertUidToString(uid)
            await sendKeyToBox(uidString)

# Wird von Thread_ReadFromCardreader aufgerufen, wenn eine Karte erkannt wird. Die uid enthält ein Array von 6 Bytes [0xF2, 0x3E, usw.]
def convertUidToString(uidByteArray):
    return str(uidByteArray, 'utf-8')


async def sendKeyToBox(uidString):
    async with websockets.connect(websocketServer) as websocket:
        await websocket.send(uidString)
        response = await websocket.recv()
        print(response)


asyncio.run(ReadFromCardreader())