import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime

st.set_page_config(
    page_title="Mundialista 2026 - Polla",
    page_icon="⚽",
    layout="wide"
)

DB = "mundialista2026_simple.db"

PARTIDOS_INICIALES = [
    {
        'match_number': 1,
        'fecha_partido': '2026-06-11 14:00:00',
        'stage': 'Grupo A',
        'home_team': 'México',
        'away_team': 'Sudáfrica',
        'estadio': 'Estadio Azteca',
        'ciudad': 'Ciudad de México'
    },
    {
        'match_number': 2,
        'fecha_partido': '2026-06-11 21:00:00',
        'stage': 'Grupo A',
        'home_team': 'Corea del Sur',
        'away_team': 'República Checa',
        'estadio': 'Estadio Guadalajara',
        'ciudad': 'Guadalajara'
    },
    {
        'match_number': 3,
        'fecha_partido': '2026-06-12 14:00:00',
        'stage': 'Grupo B',
        'home_team': 'Canadá',
        'away_team': 'Bosnia y Herzegovina',
        'estadio': 'Toronto Stadium',
        'ciudad': 'Toronto'
    },
    {
        'match_number': 4,
        'fecha_partido': '2026-06-12 20:00:00',
        'stage': 'Grupo D',
        'home_team': 'Estados Unidos',
        'away_team': 'Paraguay',
        'estadio': 'Los Angeles Stadium',
        'ciudad': 'Inglewood'
    },
    {
        'match_number': 5,
        'fecha_partido': '2026-06-13 14:00:00',
        'stage': 'Grupo B',
        'home_team': 'Catar',
        'away_team': 'Suiza',
        'estadio': 'San Francisco Bay Area Stadium',
        'ciudad': 'Santa Clara'
    },
    {
        'match_number': 6,
        'fecha_partido': '2026-06-13 17:00:00',
        'stage': 'Grupo C',
        'home_team': 'Brasil',
        'away_team': 'Marruecos',
        'estadio': 'New York New Jersey Stadium',
        'ciudad': 'East Rutherford'
    },
    {
        'match_number': 7,
        'fecha_partido': '2026-06-13 20:00:00',
        'stage': 'Grupo C',
        'home_team': 'Haití',
        'away_team': 'Escocia',
        'estadio': 'Boston Stadium',
        'ciudad': 'Foxborough'
    },
    {
        'match_number': 8,
        'fecha_partido': '2026-06-13 23:00:00',
        'stage': 'Grupo D',
        'home_team': 'Australia',
        'away_team': 'Turquía',
        'estadio': 'BC Place',
        'ciudad': 'Vancouver'
    },
    {
        'match_number': 9,
        'fecha_partido': '2026-06-14 12:00:00',
        'stage': 'Grupo E',
        'home_team': 'Alemania',
        'away_team': 'Curaçao',
        'estadio': 'Houston Stadium',
        'ciudad': 'Houston'
    },
    {
        'match_number': 10,
        'fecha_partido': '2026-06-14 15:00:00',
        'stage': 'Grupo F',
        'home_team': 'Países Bajos',
        'away_team': 'Japón',
        'estadio': 'Dallas Stadium',
        'ciudad': 'Arlington'
    },
    {
        'match_number': 11,
        'fecha_partido': '2026-06-14 18:00:00',
        'stage': 'Grupo E',
        'home_team': 'Costa de Marfil',
        'away_team': 'Ecuador',
        'estadio': 'Philadelphia Stadium',
        'ciudad': 'Filadelfia'
    },
    {
        'match_number': 12,
        'fecha_partido': '2026-06-14 21:00:00',
        'stage': 'Grupo F',
        'home_team': 'Suecia',
        'away_team': 'Túnez',
        'estadio': 'Estadio Monterrey',
        'ciudad': 'Guadalupe'
    },
    {
        'match_number': 13,
        'fecha_partido': '2026-06-15 11:00:00',
        'stage': 'Grupo H',
        'home_team': 'España',
        'away_team': 'Cabo Verde',
        'estadio': 'Atlanta Stadium',
        'ciudad': 'Atlanta'
    },
    {
        'match_number': 14,
        'fecha_partido': '2026-06-15 14:00:00',
        'stage': 'Grupo G',
        'home_team': 'Bélgica',
        'away_team': 'Egipto',
        'estadio': 'Seattle Stadium',
        'ciudad': 'Seattle'
    },
    {
        'match_number': 15,
        'fecha_partido': '2026-06-15 17:00:00',
        'stage': 'Grupo H',
        'home_team': 'Arabia Saudita',
        'away_team': 'Uruguay',
        'estadio': 'Miami Stadium',
        'ciudad': 'Miami Gardens'
    },
    {
        'match_number': 16,
        'fecha_partido': '2026-06-15 20:00:00',
        'stage': 'Grupo G',
        'home_team': 'Irán',
        'away_team': 'Nueva Zelanda',
        'estadio': 'Los Angeles Stadium',
        'ciudad': 'Inglewood'
    },
    {
        'match_number': 17,
        'fecha_partido': '2026-06-16 14:00:00',
        'stage': 'Grupo I',
        'home_team': 'Francia',
        'away_team': 'Senegal',
        'estadio': 'New York New Jersey Stadium',
        'ciudad': 'East Rutherford'
    },
    {
        'match_number': 18,
        'fecha_partido': '2026-06-16 17:00:00',
        'stage': 'Grupo I',
        'home_team': 'Irak',
        'away_team': 'Noruega',
        'estadio': 'Boston Stadium',
        'ciudad': 'Foxborough'
    },
    {
        'match_number': 19,
        'fecha_partido': '2026-06-16 20:00:00',
        'stage': 'Grupo J',
        'home_team': 'Argentina',
        'away_team': 'Argelia',
        'estadio': 'Kansas City Stadium',
        'ciudad': 'Kansas City'
    },
    {
        'match_number': 20,
        'fecha_partido': '2026-06-16 23:00:00',
        'stage': 'Grupo J',
        'home_team': 'Austria',
        'away_team': 'Jordania',
        'estadio': 'San Francisco Bay Area Stadium',
        'ciudad': 'Santa Clara'
    },
    {
        'match_number': 21,
        'fecha_partido': '2026-06-17 21:00:00',
        'stage': 'Grupo K',
        'home_team': 'Uzbekistán',
        'away_team': 'Colombia',
        'estadio': 'Estadio Azteca',
        'ciudad': 'Ciudad de México'
    },
    {
        'match_number': 22,
        'fecha_partido': '2026-06-23 21:00:00',
        'stage': 'Grupo K',
        'home_team': 'Colombia',
        'away_team': 'RD Congo',
        'estadio': 'Estadio Guadalajara',
        'ciudad': 'Guadalajara'
    },
    {
        'match_number': 23,
        'fecha_partido': '2026-06-27 18:30:00',
        'stage': 'Grupo K',
        'home_team': 'Colombia',
        'away_team': 'Portugal',
        'estadio': 'Hard Rock Stadium',
        'ciudad': 'Miami Gardens'
    },
    {
        'match_number': 24,
        'fecha_partido': '2026-06-19 14:00:00',
        'stage': 'Grupo A',
        'home_team': 'Uruguay',
        'away_team': 'España',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 25,
        'fecha_partido': '2026-06-20 18:00:00',
        'stage': 'Grupo B',
        'home_team': 'Bélgica',
        'away_team': 'Irán',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 26,
        'fecha_partido': '2026-06-21 14:00:00',
        'stage': 'Grupo C',
        'home_team': 'Francia',
        'away_team': 'Noruega',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 27,
        'fecha_partido': '2026-06-22 18:00:00',
        'stage': 'Grupo D',
        'home_team': 'Argentina',
        'away_team': 'Austria',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 28,
        'fecha_partido': '2026-06-23 14:00:00',
        'stage': 'Grupo E',
        'home_team': 'Marruecos',
        'away_team': 'Escocia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 29,
        'fecha_partido': '2026-06-24 18:00:00',
        'stage': 'Grupo F',
        'home_team': 'Suiza',
        'away_team': 'Canadá',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 30,
        'fecha_partido': '2026-06-15 14:00:00',
        'stage': 'Grupo G',
        'home_team': 'Paraguay',
        'away_team': 'Australia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 31,
        'fecha_partido': '2026-06-16 18:00:00',
        'stage': 'Grupo H',
        'home_team': 'Japón',
        'away_team': 'Suecia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 32,
        'fecha_partido': '2026-06-17 14:00:00',
        'stage': 'Grupo I',
        'home_team': 'Alemania',
        'away_team': 'Ecuador',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 33,
        'fecha_partido': '2026-06-18 18:00:00',
        'stage': 'Grupo J',
        'home_team': 'Costa de Marfil',
        'away_team': 'Curaçao',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 34,
        'fecha_partido': '2026-06-19 14:00:00',
        'stage': 'Grupo K',
        'home_team': 'Países Bajos',
        'away_team': 'Túnez',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 35,
        'fecha_partido': '2026-06-20 18:00:00',
        'stage': 'Grupo L',
        'home_team': 'Marruecos',
        'away_team': 'Brasil',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 36,
        'fecha_partido': '2026-06-21 14:00:00',
        'stage': 'Grupo A',
        'home_team': 'Egipto',
        'away_team': 'Nueva Zelanda',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 37,
        'fecha_partido': '2026-06-22 18:00:00',
        'stage': 'Grupo B',
        'home_team': 'Senegal',
        'away_team': 'Irak',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 38,
        'fecha_partido': '2026-06-23 14:00:00',
        'stage': 'Grupo C',
        'home_team': 'Argelia',
        'away_team': 'Jordania',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 39,
        'fecha_partido': '2026-06-24 18:00:00',
        'stage': 'Grupo D',
        'home_team': 'Portugal',
        'away_team': 'RD Congo',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 40,
        'fecha_partido': '2026-06-15 14:00:00',
        'stage': 'Grupo E',
        'home_team': 'Chile',
        'away_team': 'Ghana',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 41,
        'fecha_partido': '2026-06-16 18:00:00',
        'stage': 'Grupo F',
        'home_team': 'Ucrania',
        'away_team': 'Camerún',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 42,
        'fecha_partido': '2026-06-17 14:00:00',
        'stage': 'Grupo G',
        'home_team': 'Gales',
        'away_team': 'Perú',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 43,
        'fecha_partido': '2026-06-18 18:00:00',
        'stage': 'Grupo H',
        'home_team': 'Polonia',
        'away_team': 'Nigeria',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 44,
        'fecha_partido': '2026-06-19 14:00:00',
        'stage': 'Grupo I',
        'home_team': 'México',
        'away_team': 'Corea del Sur',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 45,
        'fecha_partido': '2026-06-20 18:00:00',
        'stage': 'Grupo J',
        'home_team': 'Sudáfrica',
        'away_team': 'República Checa',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 46,
        'fecha_partido': '2026-06-21 14:00:00',
        'stage': 'Grupo K',
        'home_team': 'Canadá',
        'away_team': 'Catar',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 47,
        'fecha_partido': '2026-06-22 18:00:00',
        'stage': 'Grupo L',
        'home_team': 'Bosnia y Herzegovina',
        'away_team': 'Suiza',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 48,
        'fecha_partido': '2026-06-23 14:00:00',
        'stage': 'Grupo A',
        'home_team': 'Estados Unidos',
        'away_team': 'Australia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 49,
        'fecha_partido': '2026-06-24 18:00:00',
        'stage': 'Grupo B',
        'home_team': 'Paraguay',
        'away_team': 'Turquía',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 50,
        'fecha_partido': '2026-06-15 14:00:00',
        'stage': 'Grupo C',
        'home_team': 'Brasil',
        'away_team': 'Haití',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 51,
        'fecha_partido': '2026-06-16 18:00:00',
        'stage': 'Grupo D',
        'home_team': 'Marruecos',
        'away_team': 'Escocia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 52,
        'fecha_partido': '2026-06-17 14:00:00',
        'stage': 'Grupo E',
        'home_team': 'Alemania',
        'away_team': 'Costa de Marfil',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 53,
        'fecha_partido': '2026-06-18 18:00:00',
        'stage': 'Grupo F',
        'home_team': 'Curaçao',
        'away_team': 'Ecuador',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 54,
        'fecha_partido': '2026-06-19 14:00:00',
        'stage': 'Grupo G',
        'home_team': 'Países Bajos',
        'away_team': 'Suecia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 55,
        'fecha_partido': '2026-06-20 18:00:00',
        'stage': 'Grupo H',
        'home_team': 'Japón',
        'away_team': 'Túnez',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 56,
        'fecha_partido': '2026-06-21 14:00:00',
        'stage': 'Grupo I',
        'home_team': 'España',
        'away_team': 'Arabia Saudita',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 57,
        'fecha_partido': '2026-06-22 18:00:00',
        'stage': 'Grupo J',
        'home_team': 'Cabo Verde',
        'away_team': 'Uruguay',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 58,
        'fecha_partido': '2026-06-23 14:00:00',
        'stage': 'Grupo K',
        'home_team': 'Bélgica',
        'away_team': 'Irán',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 59,
        'fecha_partido': '2026-06-24 18:00:00',
        'stage': 'Grupo L',
        'home_team': 'Egipto',
        'away_team': 'Nueva Zelanda',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 60,
        'fecha_partido': '2026-06-15 14:00:00',
        'stage': 'Grupo A',
        'home_team': 'Francia',
        'away_team': 'Irak',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 61,
        'fecha_partido': '2026-06-16 18:00:00',
        'stage': 'Grupo B',
        'home_team': 'Senegal',
        'away_team': 'Noruega',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 62,
        'fecha_partido': '2026-06-17 14:00:00',
        'stage': 'Grupo C',
        'home_team': 'Argentina',
        'away_team': 'Austria',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 63,
        'fecha_partido': '2026-06-18 18:00:00',
        'stage': 'Grupo D',
        'home_team': 'Argelia',
        'away_team': 'Jordania',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 64,
        'fecha_partido': '2026-06-19 14:00:00',
        'stage': 'Grupo E',
        'home_team': 'Portugal',
        'away_team': 'Uzbekistán',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 65,
        'fecha_partido': '2026-06-20 18:00:00',
        'stage': 'Grupo F',
        'home_team': 'RD Congo',
        'away_team': 'Polonia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 66,
        'fecha_partido': '2026-06-21 14:00:00',
        'stage': 'Grupo G',
        'home_team': 'Inglaterra',
        'away_team': 'Croacia',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 67,
        'fecha_partido': '2026-06-22 18:00:00',
        'stage': 'Grupo H',
        'home_team': 'Ghana',
        'away_team': 'Panamá',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 68,
        'fecha_partido': '2026-06-23 14:00:00',
        'stage': 'Grupo I',
        'home_team': 'Italia',
        'away_team': 'Dinamarca',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 69,
        'fecha_partido': '2026-06-24 18:00:00',
        'stage': 'Grupo J',
        'home_team': 'Serbia',
        'away_team': 'Jamaica',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 70,
        'fecha_partido': '2026-06-15 14:00:00',
        'stage': 'Grupo K',
        'home_team': 'Irlanda',
        'away_team': 'Mali',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 71,
        'fecha_partido': '2026-06-16 18:00:00',
        'stage': 'Grupo L',
        'home_team': 'Islandia',
        'away_team': 'Honduras',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 72,
        'fecha_partido': '2026-06-17 14:00:00',
        'stage': 'Grupo A',
        'home_team': 'México',
        'away_team': 'República Checa',
        'estadio': 'Estadio Mundialista',
        'ciudad': 'Sede Oficial'
    },
    {
        'match_number': 73,
        'fecha_partido': '2026-06-29 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo A',
        'away_team': '2° del Grupo C o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 74,
        'fecha_partido': '2026-06-30 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo B',
        'away_team': '2° del Grupo D o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 75,
        'fecha_partido': '2026-06-31 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo C',
        'away_team': '2° del Grupo E o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 76,
        'fecha_partido': '2026-06-28 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo D',
        'away_team': '2° del Grupo F o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 77,
        'fecha_partido': '2026-06-29 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo E',
        'away_team': '2° del Grupo G o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 78,
        'fecha_partido': '2026-06-30 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo F',
        'away_team': '2° del Grupo H o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 79,
        'fecha_partido': '2026-06-31 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo G',
        'away_team': '2° del Grupo I o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 80,
        'fecha_partido': '2026-06-28 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo H',
        'away_team': '2° del Grupo J o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 81,
        'fecha_partido': '2026-06-29 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo I',
        'away_team': '2° del Grupo K o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 82,
        'fecha_partido': '2026-06-30 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo J',
        'away_team': '2° del Grupo L o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 83,
        'fecha_partido': '2026-06-31 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo K',
        'away_team': '2° del Grupo A o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 84,
        'fecha_partido': '2026-06-28 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo L',
        'away_team': '2° del Grupo B o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 85,
        'fecha_partido': '2026-06-29 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo A',
        'away_team': '2° del Grupo C o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 86,
        'fecha_partido': '2026-06-30 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo B',
        'away_team': '2° del Grupo D o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 87,
        'fecha_partido': '2026-06-31 19:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo C',
        'away_team': '2° del Grupo E o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 88,
        'fecha_partido': '2026-06-28 15:00:00',
        'stage': 'Dieciseisavos de Final',
        'home_team': '1° del Grupo D',
        'away_team': '2° del Grupo F o Mejor 3°',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 89,
        'fecha_partido': '2026-07-05 18:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 73',
        'away_team': 'Ganador Partido 74',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 90,
        'fecha_partido': '2026-07-06 14:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 74',
        'away_team': 'Ganador Partido 75',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 91,
        'fecha_partido': '2026-07-07 18:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 75',
        'away_team': 'Ganador Partido 76',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 92,
        'fecha_partido': '2026-07-04 14:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 76',
        'away_team': 'Ganador Partido 77',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 93,
        'fecha_partido': '2026-07-05 18:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 77',
        'away_team': 'Ganador Partido 78',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 94,
        'fecha_partido': '2026-07-06 14:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 78',
        'away_team': 'Ganador Partido 79',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 95,
        'fecha_partido': '2026-07-07 18:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 79',
        'away_team': 'Ganador Partido 80',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 96,
        'fecha_partido': '2026-07-04 14:00:00',
        'stage': 'Octavos de Final',
        'home_team': 'Ganador Partido 80',
        'away_team': 'Ganador Partido 81',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 97,
        'fecha_partido': '2026-07-10 19:00:00',
        'stage': 'Cuartos de Final',
        'home_team': 'Ganador Octavos P89',
        'away_team': 'Ganador Octavos P90',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 98,
        'fecha_partido': '2026-07-09 15:00:00',
        'stage': 'Cuartos de Final',
        'home_team': 'Ganador Octavos P90',
        'away_team': 'Ganador Octavos P91',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 99,
        'fecha_partido': '2026-07-10 19:00:00',
        'stage': 'Cuartos de Final',
        'home_team': 'Ganador Octavos P91',
        'away_team': 'Ganador Octavos P92',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 100,
        'fecha_partido': '2026-07-09 15:00:00',
        'stage': 'Cuartos de Final',
        'home_team': 'Ganador Octavos P92',
        'away_team': 'Ganador Octavos P93',
        'estadio': 'Por definir',
        'ciudad': 'Sede por definir'
    },
    {
        'match_number': 101,
        'fecha_partido': '2026-07-14 19:00:00',
        'stage': 'Semifinal',
        'home_team': 'Ganador Cuartos P97',
        'away_team': 'Ganador Cuartos P98',
        'estadio': 'Dallas Stadium',
        'ciudad': 'Arlington'
    },
    {
        'match_number': 102,
        'fecha_partido': '2026-07-15 19:00:00',
        'stage': 'Semifinal',
        'home_team': 'Ganador Cuartos P99',
        'away_team': 'Ganador Cuartos P100',
        'estadio': 'Atlanta Stadium',
        'ciudad': 'Atlanta'
    },
    {
        'match_number': 103,
        'fecha_partido': '2026-07-18 15:00:00',
        'stage': 'Tercer Puesto',
        'home_team': 'Perdedor Semifinal 101',
        'away_team': 'Perdedor Semifinal 102',
        'estadio': 'Miami Stadium',
        'ciudad': 'Miami Gardens'
    },
    {
        'match_number': 104,
        'fecha_partido': '2026-07-19 15:00:00',
        'stage': 'Gran Final',
        'home_team': 'Ganador Semifinal 101',
        'away_team': 'Ganador Semifinal 102',
        'estadio': 'New York New Jersey Stadium',
        'ciudad': 'East Rutherford'
    }
]

conn = sqlite3.connect(DB, check_same_thread=False)
cur = conn.cursor()


def hash_pw(pw: str):
    return hashlib.sha256(pw.encode()).hexdigest()


def parse_dt(txt):
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            return datetime.strptime(str(txt), fmt)
        except Exception:
            pass
    return None


def fmt_dt(txt):
    dt = parse_dt(txt)
    if dt:
        return dt.strftime("%d/%m/%Y %H:%M")
    return str(txt)


def score_text(home, away):
    if pd.notna(home) and pd.notna(away):
        return f"{int(home)} - {int(away)}"
    return "-"


def init_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            admin INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_number INTEGER UNIQUE NOT NULL,
            fecha_partido TEXT NOT NULL,
            stage TEXT,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            estadio TEXT,
            ciudad TEXT,
            home_score INTEGER,
            away_score INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            home_pred INTEGER NOT NULL,
            away_pred INTEGER NOT NULL,
            puntos INTEGER DEFAULT 0,
            locked INTEGER DEFAULT 1,
            created_at TEXT,
            UNIQUE(user_id, match_id)
        )
    """)
    conn.commit()

    cur.execute("SELECT id FROM users WHERE correo=?", ("brallanhernandez460@gmail.com",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (nombre, correo, password_hash, admin, created_at) VALUES (?, ?, ?, 1, ?)",
            (
                "Administrador",
                "brallanhernandez460@gmail.com",
                hash_pw("Roman0511+"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()


def seed_matches_if_empty():
    cur.execute("SELECT COUNT(*) FROM matches")
    total = cur.fetchone()[0]

    if total == 0:
        for m in PARTIDOS_INICIALES:
            cur.execute(
                """
                INSERT INTO matches (
                    match_number,
                    fecha_partido,
                    stage,
                    home_team,
                    away_team,
                    estadio,
                    ciudad
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    m["match_number"],
                    m["fecha_partido"],
                    m["stage"],
                    m["home_team"],
                    m["away_team"],
                    m["estadio"],
                    m["ciudad"]
                )
            )
        conn.commit()


def existe_usuario(correo):
    cur.execute("SELECT id FROM users WHERE correo=?", (correo.strip().lower(),))
    return cur.fetchone()


def crear_usuario(nombre, correo, password, admin=0):
    cur.execute(
        "INSERT INTO users (nombre, correo, password_hash, admin, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            nombre,
            correo.strip().lower(),
            hash_pw(password),
            admin,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    conn.commit()


def login(correo, password):
    cur.execute(
        "SELECT id, nombre, correo, admin FROM users WHERE correo=? AND password_hash=?",
        (correo.strip().lower(), hash_pw(password))
    )
    return cur.fetchone()


def get_matches(search=""):
    df = pd.read_sql_query("SELECT * FROM matches ORDER BY match_number", conn)

    if len(df) > 0:
        df["_dt"] = pd.to_datetime(df["fecha_partido"], errors="coerce")
        df = df.sort_values(by=["_dt", "match_number"], na_position="last").drop(columns=["_dt"])

        if search:
            s = search.lower().strip()
            df = df[
                df["home_team"].str.lower().str.contains(s, na=False)
                | df["away_team"].str.lower().str.contains(s, na=False)
                | df["stage"].str.lower().str.contains(s, na=False)
                | df["match_number"].astype(str).str.contains(s, na=False)
            ]

    return df


def prediction_exists(user_id, match_id):
    cur.execute("SELECT id FROM predictions WHERE user_id=? AND match_id=?", (user_id, match_id))
    return cur.fetchone()


def guardar_prediccion(user_id, match_id, home_pred, away_pred):
    if prediction_exists(user_id, match_id):
        raise ValueError("Ese partido ya lo registraste y quedó bloqueado y no se puede cambiar.")

    cur.execute(
        """
        INSERT INTO predictions (
            user_id,
            match_id,
            home_pred,
            away_pred,
            puntos,
            locked,
            created_at
        ) VALUES (?, ?, ?, ?, 0, 1, ?)
        """,
        (
            user_id,
            match_id,
            int(home_pred),
            int(away_pred),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    conn.commit()


def get_user_predictions(user_id):
    return pd.read_sql_query("""
        SELECT
            p.id,
            m.match_number,
            m.fecha_partido,
            m.stage,
            m.home_team,
            m.away_team,
            m.home_score,
            m.away_score,
            p.home_pred,
            p.away_pred,
            p.puntos,
            p.created_at
        FROM predictions p
        JOIN matches m ON m.id = p.match_id
        WHERE p.user_id = ?
        ORDER BY m.match_number
    """, conn, params=(user_id,))


def calcular_puntos(home_pred, away_pred, home_score, away_score):
    home_pred = int(home_pred)
    away_pred = int(away_pred)
    home_score = int(home_score)
    away_score = int(away_score)

    # 3 puntos si acierta exacto
    if home_pred == home_score and away_pred == away_score:
        return 3

    # Resultado del pronóstico
    if home_pred > away_pred:
        resultado_pred = "L"   # local
    elif home_pred < away_pred:
        resultado_pred = "V"   # visitante
    else:
        resultado_pred = "E"   # empate

    # Resultado oficial
    if home_score > away_score:
        resultado_real = "L"
    elif home_score < away_score:
        resultado_real = "V"
    else:
        resultado_real = "E"

    # 1 punto si acierta ganador o empate
    if resultado_pred == resultado_real:
        return 1

    # 0 si no acierta nada
    return 0


def recalcular_puntos_partido(match_id):
    preds = pd.read_sql_query("""
        SELECT id, home_pred, away_pred
        FROM predictions
        WHERE match_id = ?
    """, conn, params=(match_id,))

    match_df = pd.read_sql_query("""
        SELECT home_score, away_score
        FROM matches
        WHERE id = ?
    """, conn, params=(match_id,))

    if len(match_df) == 0:
        return

    home_score = match_df.iloc[0]["home_score"]
    away_score = match_df.iloc[0]["away_score"]

    if pd.isna(home_score) or pd.isna(away_score):
        return

    for _, pr in preds.iterrows():
        puntos = calcular_puntos(
            pr["home_pred"],
            pr["away_pred"],
            home_score,
            away_score
        )
        cur.execute(
            "UPDATE predictions SET puntos=? WHERE id=?",
            (int(puntos), int(pr["id"]))
        )

    conn.commit()


def actualizar_resultado_oficial(match_id, home_score, away_score):
    cur.execute(
        "UPDATE matches SET home_score=?, away_score=? WHERE id=?",
        (int(home_score), int(away_score), int(match_id))
    )
    conn.commit()

    # Recalcular automáticamente los puntos del partido
    recalcular_puntos_partido(match_id)


def get_predictions_by_match(match_id):
    return pd.read_sql_query("""
        SELECT
            p.id,
            u.nombre,
            p.home_pred,
            p.away_pred,
            p.puntos,
            p.created_at
        FROM predictions p
        JOIN users u ON u.id = p.user_id
        WHERE p.match_id = ? AND u.admin = 0
        ORDER BY u.nombre
    """, conn, params=(match_id,))


def get_ranking():
    return pd.read_sql_query("""
        SELECT
            u.nombre,
            COALESCE(SUM(p.puntos), 0) AS puntos,
            COALESCE(COUNT(p.id), 0) AS pronosticos
        FROM users u
        LEFT JOIN predictions p ON p.user_id = u.id
        WHERE u.admin = 0
        GROUP BY u.id, u.nombre
        ORDER BY puntos DESC, pronosticos DESC, u.nombre ASC
    """, conn)


init_db()
seed_matches_if_empty()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("⚽ Polla - Mundialista 2026")
st.caption("Polla para registrar tus pronósticos del Mundial 2026. ¡Que gane el mejor!")

if st.session_state.user is None:
    t1, t2 = st.tabs(["🔑 Iniciar sesión", "📝 Crear usuario"])

    with t1:
        correo = st.text_input("Correo", key="login_correo")
        pw = st.text_input("Contraseña", type="password", key="login_pw")

        if st.button("Entrar", use_container_width=True):
            u = login(correo, pw)
            if u:
                st.session_state.user = {
                    "id": u[0],
                    "nombre": u[1],
                    "correo": u[2],
                    "admin": u[3]
                }
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

        st.info("User")

    with t2:
        nombre = st.text_input("Nombre completo", key="reg_nombre")
        correo = st.text_input("Correo", key="reg_correo")
        pw1 = st.text_input("Contraseña", type="password", key="reg_pw1")
        pw2 = st.text_input("Confirmar contraseña", type="password", key="reg_pw2")

        if st.button("Crear usuario", use_container_width=True):
            if not nombre or not correo or not pw1:
                st.warning("Completa todos los campos.")
            elif pw1 != pw2:
                st.warning("Las contraseñas no coinciden.")
            elif existe_usuario(correo):
                st.warning("Ese correo ya está registrado.")
            else:
                crear_usuario(nombre, correo, pw1)
                st.success("✅ Usuario creado. Ya puedes iniciar sesión.")

else:
    user = st.session_state.user

    h1, h2 = st.columns([6, 1])

    with h1:
        st.success(f"👋 {user['nombre']}")

    with h2:
        if st.button("Salir", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    tabs = st.tabs(["🎯 Partidos", "🏆 Ranking"])

    with tabs[0]:
        search = st.text_input("🔎 Buscar partido por equipo o número", key="buscar_partido")
        df_matches = get_matches(search)

        if len(df_matches) == 0:
            st.info("No se encontraron partidos.")
        else:
            df_matches = df_matches.copy()
            df_matches["label"] = df_matches.apply(
                lambda r: f"#{int(r['match_number'])} | {fmt_dt(r['fecha_partido'])} | {r['home_team']} vs {r['away_team']}",
                axis=1
            )

            selected = st.selectbox(
                "Selecciona un partido",
                df_matches["label"].tolist(),
                key="match_select"
            )

            row = df_matches[df_matches["label"] == selected].iloc[0]

            st.markdown(f"**{row['home_team']} vs {row['away_team']}**")
            st.caption(f"{row['stage']} | {fmt_dt(row['fecha_partido'])} | {row['estadio']} - {row['ciudad']}")

            if user["admin"]:
                st.write("### Resultado oficial")

                c1, c2 = st.columns(2)

                hs = c1.number_input(
                    f"Goles oficiales {row['home_team']}",
                    min_value=0,
                    max_value=30,
                    value=int(row["home_score"]) if pd.notna(row["home_score"]) else 0,
                    step=1,
                    key="official_h"
                )

                aw = c2.number_input(
                    f"Goles oficiales {row['away_team']}",
                    min_value=0,
                    max_value=30,
                    value=int(row["away_score"]) if pd.notna(row["away_score"]) else 0,
                    step=1,
                    key="official_a"
                )

                if st.button("Guardar resultado oficial", key="save_official", use_container_width=True):
                    actualizar_resultado_oficial(int(row["id"]), hs, aw)
                    st.success("✅ Resultado oficial guardado y puntos calculados automáticamente.")
                    st.rerun()

                st.markdown("---")
                st.write("### Pronósticos del partido")

                preds = get_predictions_by_match(int(row["id"]))
                if len(preds) == 0:
                    st.info("No hay pronósticos para este partido.")
                else:
                    for _, pr in preds.iterrows():
                        with st.container(border=True):
                            st.write(f"**{pr['nombre']}**")
                            st.caption(
                                f"Pronóstico: {int(pr['home_pred'])} - {int(pr['away_pred'])} | "
                                f"Puntos: {int(pr['puntos']) if pd.notna(pr['puntos']) else 0}"
                                f"Registrado: {fmt_dt(pr['created_at'])}"
                            )

            else:
                st.write("### Tu pronóstico")

                existing = prediction_exists(user["id"], int(row["id"]))
                if existing:
                    st.info("Ya registraste este partido. El pronóstico quedó bloqueado y no se puede cambiar.")
                else:
                    c1, c2 = st.columns(2)

                    hp = c1.number_input(
                        f"Goles {row['home_team']}",
                        min_value=0,
                        max_value=30,
                        value=0,
                        step=1,
                        key="pred_h"
                    )

                    ap = c2.number_input(
                        f"Goles {row['away_team']}",
                        min_value=0,
                        max_value=30,
                        value=0,
                        step=1,
                        key="pred_a"
                    )

                    if st.button("Guardar mi pronóstico", use_container_width=True):
                        try:
                            guardar_prediccion(user["id"], int(row["id"]), hp, ap)
                            st.success("✅ Pronóstico guardado y bloqueado.")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

                st.markdown("---")
                st.write("### Mis pronósticos")

                my_preds = get_user_predictions(user["id"])
                if len(my_preds) > 0:
                    disp = my_preds.copy()
                    disp["Fecha"] = disp["fecha_partido"].apply(fmt_dt)
                    disp["Fecha registro"] = disp["created_at"].apply(fmt_dt)
                    disp["Mi pronóstico"] = disp.apply(
                        lambda r: f"{int(r['home_pred'])} - {int(r['away_pred'])}",
                        axis=1
                    )
                    disp["Resultado oficial"] = disp.apply(
                        lambda r: score_text(r["home_score"], r["away_score"]),
                        axis=1
                    )

                    st.dataframe(
                        disp[
                            [
                                "match_number",
                                "Fecha",
                                "Fecha registro",
                                "stage",
                                "home_team",
                                "away_team",
                                "Mi pronóstico",
                                "Resultado oficial",
                                "puntos"
                            ]
                        ].rename(columns={
                            "match_number": "#",
                            "stage": "Fase",
                            "home_team": "Local",
                            "away_team": "Visitante",
                            "puntos": "Puntos"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("Aún no has registrado pronósticos.")

    with tabs[1]:
        st.subheader("Ranking general")
        rank = get_ranking()

        if len(rank) > 0:
            rank = rank.reset_index(drop=True)
            rank.index = rank.index + 1
            rank["Posición"] = rank.index

            st.dataframe(
                rank[["Posición", "nombre", "puntos", "pronosticos"]].rename(columns={
                    "nombre": "Nombre",
                    "puntos": "Puntos",
                    "pronosticos": "Pronósticos"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aún no hay datos para el ranking.")