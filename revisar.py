import sqlite3
import os

# Buscar TODOS los archivos .db en el proyecto
print("=== BUSCANDO BASES DE DATOS ===")
for root, dirs, files in os.walk('/workspaces'):
    for f in files:
        if f.endswith('.db'):
            ruta = os.path.join(root, f)
            size = os.path.getsize(ruta)
            print(f"  {ruta} ({size} bytes)")
            
            # Ver cuántos registros tiene cada una
            try:
                conn = sqlite3.connect(ruta)
                c = conn.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table'")
                for t in c.fetchall():
                    c.execute(f"SELECT COUNT(*) FROM {t[0]}")
                    total = c.fetchone()[0]
                    if total > 0:
                        print(f"    {t[0]}: {total} registros")
                conn.close()
            except:
                pass