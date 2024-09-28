from flask import render_template, request, send_file
import pandas as pd
import io
import zipfile
from ErzieherKonvertierer import app

@app.route('/')
def upload_files():
    app.logger.info("Rendering upload.html")
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_files():
    try:
        # Dateien aus dem Formular abrufen
        erzieher_export_file = request.files['erzieher_export_file']
        ansprechpartner_export_file = request.files['ansprechpartner_export_file']

        app.logger.info("Dateien erhalten: %s, %s", erzieher_export_file.filename, ansprechpartner_export_file.filename)

        # Daten einlesen mit dem richtigen Trennzeichen (;)
        erzieher_export_df = pd.read_csv(erzieher_export_file, sep=';', encoding='utf-8')
        ansprechpartner_export_df = pd.read_csv(ansprechpartner_export_file, sep=';', encoding='utf-8')

        # Alle Spaltennamen bereinigen, um sicherzustellen, dass keine unnötigen Leerzeichen vorhanden sind
        erzieher_export_df.columns = erzieher_export_df.columns.str.strip()
        ansprechpartner_export_df.columns = ansprechpartner_export_df.columns.str.strip()

        # Spaltennamen anzeigen
        app.logger.info("Spaltennamen des Erzieher-Exports: %s", erzieher_export_df.columns.tolist())
        app.logger.info("Spaltennamen des Ansprechpartner-Exports: %s", ansprechpartner_export_df.columns.tolist())

        # Korrektes Umbenennen der Spalten
        if 'Interne ID-Nummer' in erzieher_export_df.columns:
            erzieher_export_df.rename(columns={'Interne ID-Nummer': 'Interne_ID_Nummer'}, inplace=True)
        else:
            raise ValueError("Die Spalte 'Interne ID-Nummer' konnte nicht im Erzieher-Export gefunden werden.")

        if 'Schüler_ID' in ansprechpartner_export_df.columns:
            ansprechpartner_export_df.rename(columns={'Schüler_ID': 'Interne_ID_Nummer'}, inplace=True)
        else:
            raise ValueError("Die Spalte 'Schüler_ID' konnte nicht im Ansprechpartner-Export gefunden werden.")

        # Spaltennamen nach Umbenennung anzeigen
        app.logger.info("Erzieher-Export Spalten nach Umbenennung: %s", erzieher_export_df.columns.tolist())
        app.logger.info("Ansprechpartner-Export Spalten nach Umbenennung: %s", ansprechpartner_export_df.columns.tolist())

        # Daten verarbeiten
        result_files = verarbeite_daten(erzieher_export_df, ansprechpartner_export_df)

        # Ergebnisdateien als ZIP zum Download anbieten
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename, df in result_files.items():
                data = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
                zf.writestr(f"{filename}.csv", data)
        memory_file.seek(0)

        return send_file(memory_file, download_name='Ergebnisdateien.zip', as_attachment=True)
    except Exception as e:
        app.logger.error("Fehler beim Verarbeiten der Dateien: %s", e)
        return f"Es ist ein Fehler aufgetreten: {e}", 500

def verarbeite_daten(erzieher_export_df, ansprechpartner_export_df):
    # Umbenennen der Spalten in der Ansprechpartner-Export-Datei zur Verknüpfung
    ansprechpartner_export_df.rename(columns={'Schüler_ID': 'Interne_ID_Nummer'}, inplace=True)

    # Sortiere nach Interne_ID_Nummer, damit die Ansprechpartner-Daten in der korrekten Reihenfolge sind
    ansprechpartner_export_df.sort_values(by=['Interne_ID_Nummer'], inplace=True)
    
    # Füge eine neue Spalte hinzu, die die laufende Nummer des Erziehers pro Schüler-ID festlegt
    ansprechpartner_export_df['Erzieher_Nummer'] = ansprechpartner_export_df.groupby('Interne_ID_Nummer').cumcount() + 1

    # Initialisiere ein Dictionary für die Ergebnisdateien
    result_files = {}

    # Bestimme die maximale Anzahl an Erziehern für einen Schüler
    max_erzieher = ansprechpartner_export_df['Erzieher_Nummer'].max()
    
    # Gehe durch alle möglichen Erzieher (1 bis max_erzieher)
    for i in range(1, max_erzieher + 1):
        # Dynamisch Spaltennamen für den jeweiligen Erzieher vorbereiten
        erzieher_columns = [
            f'Erzieher {i}: Anrede', f'Erzieher {i}: Briefanrede', f'Erzieher {i}: Titel', 
            f'Erzieher {i}: Nachname', f'Erzieher {i}: Vorname', f'Erzieher {i}: E-Mail'
        ]
        
        # Sicherstellen, dass die Spalten für Erzieher i im erzieher_export_df existieren
        for col in erzieher_columns:
            if col not in erzieher_export_df.columns:
                erzieher_export_df[col] = ''  # Leere Spalte hinzufügen, falls sie nicht existiert
        
        # Wählen der relevanten Erzieherdaten
        erzieher_i_df = ansprechpartner_export_df[ansprechpartner_export_df['Erzieher_Nummer'] == i][[
            'Interne_ID_Nummer', 'Anschluss-Art', 'Bemerkung', 'Telefon-Nummer'
        ]]
        
        # Umbenennen der Spalten für den jeweiligen Erzieher
        erzieher_i_df.rename(columns={
            'Anschluss-Art': f'Erzieher {i}: Anschluss Art',
            'Bemerkung': f'Erzieher {i}: Bemerkung',
            'Telefon-Nummer': f'Erzieher {i}: Telefon-Nummer'
        }, inplace=True)
        
        # Zusammenführen der Erzieherdaten und der Ansprechpartnerdaten für den jeweiligen Erzieher
        erzieher_i_data = pd.merge(erzieher_export_df, erzieher_i_df, on='Interne_ID_Nummer', how='left')
        
        # Filtern, um nur die relevanten Spalten für den jeweiligen Erzieher beizubehalten
        relevant_columns = ['Interne_ID_Nummer'] + erzieher_columns + [f'Erzieher {i}: Anschluss Art', f'Erzieher {i}: Bemerkung', f'Erzieher {i}: Telefon-Nummer']
        erzieher_i_data = erzieher_i_data[relevant_columns]
        
        # Hinzufügen zur Ergebnisdatei
        result_files[f'Erzieher_{i}'] = erzieher_i_data

    return result_files
