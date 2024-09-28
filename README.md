# SchildNRW-WebUntis Erzieher-Konvertierer

## **Übersicht**

Der "SchildNRW-WebUntis Erzieher-Konvertierer" wurde entwickelt, um das Problem der getrennten Speicherung von Erziehern und Ansprechpartnern in **SchildNRW** zu lösen, sodass eine korrekte Datenübertragung nach **WebUntis** erfolgen kann.

In **SchildNRW** können zwar beliebig viele Ansprechpartner mit unterschiedlichen Telefonnummern pro Schüler hinterlegt werden, allerdings wird bei den eigentlichen Erzieher-Datensätzen nur eine einzige Telefonnummer unterstützt. WebUntis erwartet hingegen für jeden Erzieher inklusive Telefonnummern einen eigenen Datensatz, um eine reibungslose Zuordnung zu ermöglichen. Dieses Programm stellt daher sicher, dass alle Erzieherinformationen (einschließlich Telefonnummern) in einem Format aufbereitet werden, das für den Import in WebUntis geeignet ist.

## **Funktionsweise**

Der "SchildNRW-WebUntis Erzieher-Konvertierer" kombiniert Erzieherdaten aus den zwei separaten Exportdateien von **SchildNRW**:

- **Erzieher Export (Hauptdaten)** 
- **Ansprechpartner Export (Zusätzliche Daten)**

Es erzeugt für jeden Erzieher- und Ansprechpartner-Datensatz eine separate Import-Datei, die vollständig kompatibel mit WebUntis ist. Damit wird sichergestellt, dass jeder Erzieher und Ansprechpartner mit der richtigen Telefonnummer in WebUntis importiert wird.

## **Voraussetzungen**

- **Windows-Betriebssystem**: Die EXE-Datei ist für Windows vorbereitet und getestet.

## **Verwendung der Anwendung**

1. **Download der ausführbaren Datei**: 
   - Laden Sie die bereitgestellte Datei [`SchildNRW-WebUntis_Erzieher-Konvertierer.exe`](https://github.com/CmoneBK/SchildNRW-WebUntis-Erzieher-Konvertierer/blob/master/dist/SchildNRW-WebUntis_Erzieher-Konvertierer.exe) auf Ihren Computer herunter. (Der Download-Button befindet sich rechts oben neben dem "RAW".)

2. **Ausführen der EXE-Datei**:
   - Doppelklicken Sie auf `SchildNRW-WebUntis Erzieher-Konvertierer.exe`, um die Anwendung zu starten.

3. **Hochladen der Export-Dateien**:
   - Wählen Sie im ersten Feld die **Erzieher Export Datei** aus SchildNRW aus (normalerweise die Datei mit den Erzieherdaten).
   - Wählen Sie im zweiten Feld die **Ansprechpartner Export Datei** aus SchildNRW aus (normalerweise die Datei mit den zusätzlichen Ansprechpartnerdaten).
[Hier geht's zu den Schild-Exporteinstellungen](Schild-Export%20Einstellungen.md)
4. **Verarbeitung der Daten**:
   - Klicken Sie auf "Dateien hochladen und verarbeiten". Das Programm wird die Daten zusammenführen und die benötigten Importdateien erstellen.

5. **Erhalten der Importdateien**:
   - Nach erfolgreicher Verarbeitung wird eine ZIP-Datei zum Download bereitgestellt. Diese enthält die einzelnen Importdateien (`Erzieher_1.csv`, `Erzieher_2.csv`, usw.) für den Import in WebUntis.
[Hier geht's zu den WebUntis-Importeinstellungen](WebUntis-Import%20Einstellungen.md)
## **Häufige Probleme und Lösungen**

- **Problem: Die EXE-Datei lässt sich nicht ausführen oder wird blockiert.**
  - **Lösung**: Überprüfen Sie, ob Ihr Antivirus-Programm die Anwendung blockiert. Fügen Sie eine Ausnahme hinzu, falls erforderlich.

- **Problem: Fehlende Daten in den Exportdateien**
  - **Lösung**: Stellen Sie sicher, dass die SchildNRW-Exportdateien vollständig und korrekt formatiert sind, bevor Sie sie in die Anwendung hochladen.

## **Hintergrund zum Projekt**

Das Programm wurde entwickelt, um das Problem der getrennten Speicherung von Erziehern und Ansprechpartnern in SchildNRW zu lösen. Da WebUntis jeden Erzieher und Ansprechpartner als separaten Datensatz behandelt, musste eine Lösung gefunden werden, die es ermöglicht, die verschiedenen Telefonnummern korrekt in das System zu übertragen.

Durch die Konvertierung und Zusammenführung der Daten ermöglicht dieses Programm einen vollständigen und fehlerfreien Import nach WebUntis, sodass die Schulverwaltungsdaten korrekt übertragen werden können.

## **Lizenz**

Dieses Programm ist unter der MIT-Lizenz lizenziert – weitere Informationen finden Sie in der [LICENSE](LICENSE)-Datei.
