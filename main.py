import numpy as np
import time
import os
import signal
import sys
import ida
from ida import profundizar
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


TIMEOUT = 120  # segundos por instancia

class TimeoutError(Exception):
    pass

def handler_timeout(signum, frame):
    ida.set_stop()
    raise TimeoutError()


def leer_instancia(filepath):
    with open(filepath, "r") as f:
        lineas = [l.strip() for l in f if l.strip()]

    n = int(lineas[0])
    tablero_inicial = []
    tablero_destino = []

    for i in range(1, n + 1):
        fila = list(map(int, lineas[i].split(",")))
        tablero_inicial.append(fila)

    for i in range(n + 1, 2 * n + 1):
        fila = list(map(int, lineas[i].split(",")))
        tablero_destino.append(fila)

    return n, np.array(tablero_inicial), np.array(tablero_destino)


def resolver_instancia(filepath):
    nombre = os.path.basename(filepath)
    print(f"\n{'─'*50}")
    print(f"Instancia: {nombre}")

    try:
        n, inicial, destino = leer_instancia(filepath)
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return {"archivo": nombre, "estado": "error_lectura", "movimientos": None, "tiempo": None}

    print(f"  Tamaño: {n}x{n}")
    print(f"  Tablero inicial:\n{inicial}")
    print(f"  Tablero destino:\n{destino}")

    signal.signal(signal.SIGALRM, handler_timeout)
    signal.alarm(TIMEOUT)

    estado = "sin_solucion"
    movimientos = None
    tiempo = None

    try:
        inicio = time.time()
        camino = profundizar(inicial, destino, n)
        fin = time.time()
        tiempo = fin - inicio
        signal.alarm(0)

        if camino:
            movimientos = len(camino) - 1
            estado = "resuelto"
            print(f"Solución en {movimientos} movimientos | {tiempo:.4f}s")
        else:
            print(f"No se encontró solución | {tiempo:.4f}s")

    except TimeoutError:
        tiempo = TIMEOUT
        estado = "timeout"
        signal.alarm(0)
        print(f"Timeout ({TIMEOUT}s) alcanzado")

    except Exception as e:
        signal.alarm(0)
        estado = f"error: {e}"
        print(f" Error durante búsqueda: {e}")

    return {
        "archivo": nombre,
        "estado": estado,
        "movimientos": movimientos,
        "tiempo": round(tiempo, 4) if tiempo is not None else None
    }

def obtener_instancias(ruta_base, tamanios=None, dificultades=None):
    """
    Recorre data/<tamanio>/<dificultad>/instancia_XX.txt
    Retorna lista de tuplas (filepath, tamanio, dificultad)
    """
    instancias = []
    for tam in sorted(os.listdir(ruta_base)):
        if tamanios and tam not in tamanios:
            continue
        ruta_tam = os.path.join(ruta_base, tam)
        if not os.path.isdir(ruta_tam):
            continue
        for dif in sorted(os.listdir(ruta_tam)):
            if dificultades and dif not in dificultades:
                continue
            ruta_dif = os.path.join(ruta_tam, dif)
            if not os.path.isdir(ruta_dif):
                continue
            for archivo in sorted(os.listdir(ruta_dif)):
                if archivo.endswith(".txt"):
                    instancias.append((os.path.join(ruta_dif, archivo), tam, dif))
    return instancias



# ─── Dashboard por dificultad ─────────────────────────────────────────────────
def generar_graficas(resultados, tamanio_tag="nxn", dificultad="general"):
    """
    Genera un dashboard en:
        {tamanio_tag}-graficas/{dificultad}/dashboard.png

    Título coloreado según dificultad:
        facil  → verde  | medio → naranja | dificil → rojo
    """
    from matplotlib.patches import Patch

    COLOR_DIF = {"facil": "#2E7D32", "medio": "#E65100", "dificil": "#B71C1C", "general": "#1A237E"}
    color_titulo = COLOR_DIF.get(dificultad, "#1A237E")

    carpeta = os.path.join(f"{tamanio_tag}-graficas", dificultad)
    os.makedirs(carpeta, exist_ok=True)

    nombres     = [r["archivo"] for r in resultados]
    estados     = [r["estado"]  for r in resultados]
    tiempos     = [r["tiempo"]      if r["tiempo"]      is not None else 0 for r in resultados]
    movimientos = [r["movimientos"] if r["movimientos"] is not None else 0 for r in resultados]

    resueltos_mask = [e == "resuelto"     for e in estados]
    timeout_mask   = [e == "timeout"      for e in estados]
    sinsol_mask    = [e == "sin_solucion" for e in estados]
    error_mask     = [e not in ("resuelto","timeout","sin_solucion") for e in estados]

    C    = {"resuelto": "#4CAF50", "timeout": "#FF9800", "sin_solucion": "#9E9E9E", "error": "#F44336"}
    etiq = [n.replace("instancia_","#").replace(".txt","") for n in nombres]

    # ── Layout ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 11), facecolor="#F5F5F5")
    titulo = f"Dashboard  ·  {tamanio_tag}  ·  {dificultad.upper()}"
    fig.suptitle(titulo, fontsize=15, fontweight="bold", y=0.98, color=color_titulo)
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.52, wspace=0.3,
                           height_ratios=[1.1, 1, 1])

    ax_pie  = fig.add_subplot(gs[0, 0])
    ax_t    = fig.add_subplot(gs[0, 1])
    ax_p    = fig.add_subplot(gs[1, :])
    ax_temp = fig.add_subplot(gs[2, :])

    # ── 1. PASTEL ─────────────────────────────────────────────────────────────
    conteos = {"Resueltos": sum(resueltos_mask), "Timeout": sum(timeout_mask),
               "Sin sol.":  sum(sinsol_mask),    "Error":   sum(error_mask)}
    conteos = {k: v for k, v in conteos.items() if v > 0}
    ax_pie.pie(conteos.values(), labels=conteos.keys(),
               autopct="%1.0f%%", startangle=140,
               colors=["#4CAF50","#FF9800","#9E9E9E","#F44336"][:len(conteos)],
               wedgeprops=dict(edgecolor="white", linewidth=1.4),
               textprops=dict(fontsize=9))
    ax_pie.set_title("Resultados", fontsize=10, fontweight="bold")

    # ── 2. BARRAS: TIEMPO ─────────────────────────────────────────────────────
    col_barras = [C.get(e, C["error"]) for e in estados]
    ax_t.bar(range(len(etiq)), tiempos, color=col_barras, edgecolor="white", linewidth=0.6)
    ax_t.axhline(TIMEOUT, color="red", linestyle="--", linewidth=1, label=f"Timeout {TIMEOUT}s")
    ax_t.set_xticks(range(len(etiq)))
    ax_t.set_xticklabels(etiq, rotation=55, ha="right", fontsize=7)
    ax_t.set_ylabel("Tiempo (s)", fontsize=8)
    ax_t.set_title("Tiempo de ejecución", fontsize=10, fontweight="bold")
    ax_t.set_ylim(0, max(tiempos) * 1.2 + 0.5)
    ax_t.legend(fontsize=7, loc="upper left")

    # ── 3. BARRAS: PASOS ─────────────────────────────────────────────────────
    res_datos = [(e, m) for e, m, ok in zip(etiq, movimientos, resueltos_mask) if ok]
    if res_datos:
        nombres_r, movs_r = zip(*res_datos)
        bars = ax_p.bar(range(len(nombres_r)), movs_r, color="#2196F3", edgecolor="white", linewidth=0.6)
        ax_p.set_xticks(range(len(nombres_r)))
        ax_p.set_xticklabels(nombres_r, rotation=55, ha="right", fontsize=7)
        ax_p.set_ylabel("Pasos", fontsize=8)
        ax_p.set_title("Pasos para resolver (instancias resueltas)", fontsize=10, fontweight="bold")
        for bar, val in zip(bars, movs_r):
            ax_p.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                      str(val), ha="center", va="bottom", fontsize=7)
    else:
        ax_p.text(0.5, 0.5, "Sin instancias resueltas", ha="center", va="center",
                  transform=ax_p.transAxes, fontsize=11, color="gray")
        ax_p.set_title("Pasos para resolver", fontsize=10, fontweight="bold")

    # ── 4. LÍNEA: TEMPERATURA ─────────────────────────────────────────────────
    tiempos_acum = np.cumsum(tiempos)
    xs = range(len(etiq))
    ax_temp.plot(xs, tiempos_acum, color="#9C27B0", linewidth=2, zorder=2)
    ax_temp.fill_between(xs, tiempos_acum, alpha=0.12, color="#9C27B0")
    for i, (ok, to) in enumerate(zip(resueltos_mask, timeout_mask)):
        color = "#4CAF50" if ok else ("#FF9800" if to else "#9E9E9E")
        ax_temp.scatter(i, tiempos_acum[i], color=color, s=45, zorder=5)
    ax_temp.set_xticks(range(len(etiq)))
    ax_temp.set_xticklabels(etiq, rotation=55, ha="right", fontsize=7)
    ax_temp.set_ylabel("Tiempo acumulado (s)", fontsize=8)
    ax_temp.set_title("Temperatura del proceso (tiempo acumulado)", fontsize=10, fontweight="bold")
    leg = [plt.Line2D([0],[0], color="#9C27B0", lw=2, label="Acumulado"),
           Patch(color="#4CAF50", label="Resuelto"),
           Patch(color="#FF9800", label="Timeout"),
           Patch(color="#9E9E9E", label="Sin sol.")]
    ax_temp.legend(handles=leg, fontsize=7, loc="upper left", ncol=4)

    # ── Guardar ───────────────────────────────────────────────────────────────
    ruta = os.path.join(carpeta, "dashboard.png")
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[{dificultad:8s}] Dashboard → {ruta}")

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    RUTA_DATA = "data"

    # ── Filtra aquí si quieres procesar solo ciertos tamaños/dificultades ──
    TAMANIOS     = ["6x6"]   # ej. ["3x3", "4x4"]  o None para todas
    DIFICULTADES =  ["facil","medio","dificil"]   #inicamos facil medio dificil 

    instancias = obtener_instancias(RUTA_DATA, TAMANIOS, DIFICULTADES)

    if not instancias:
        print("No se encontraron instancias. Verifica la ruta 'data/'.")
        sys.exit(1)

    print("{len(instancias)} instancia(s) encontradas.\n")

    # ── Resolver y agrupar por (tamanio, dificultad) ──────────────────────────
    from collections import defaultdict
    grupos = defaultdict(list)   # {(tam, dif): [resultado, ...]}
    todos  = []

    for ruta, tam, dif in instancias:
        resultado = resolver_instancia(ruta)
        resultado["dificultad"] = dif
        resultado["tamanio"]    = tam
        grupos[(tam, dif)].append(resultado)
        todos.append(resultado)

    # ── Resumen final ──────────────────────────────────────────────────────────
    resueltos = [r for r in todos if r["estado"] == "resuelto"]
    timeouts  = [r for r in todos if r["estado"] == "timeout"]
    errores   = [r for r in todos if r["estado"] not in ("resuelto", "timeout", "sin_solucion")]

    print(f"\n{'═'*50}")
    print("RESUMEN FINAL")
    print(f"Total instancias : {len(todos)}")
    print(f"Resueltas        : {len(resueltos)}")
    print(f"Timeouts         : {len(timeouts)}")
    print(f"Sin solución     : {len(todos) - len(resueltos) - len(timeouts) - len(errores)}")
    print(f"Errores          : {len(errores)}")
    if resueltos:
        tiempos_r = [r["tiempo"] for r in resueltos]
        print(f"Tiempo promedio (resueltas): {sum(tiempos_r)/len(tiempos_r):.4f}s")

    # ── Generar un dashboard por cada combinación tamaño+dificultad ───────────
    tamanio_tag = TAMANIOS[0] if TAMANIOS and len(TAMANIOS) == 1 else "nxn"

    print("\nGenerando dashboards por dificultad...")
    for (tam, dif), resultados_grupo in sorted(grupos.items()):
        generar_graficas(resultados_grupo, tamanio_tag=tam, dificultad=dif)

    print("\nGráficas en: ./{tamanio_tag}-graficas/")
    print("   ├── facil/dashboard.png")
    print("   ├── medio/dashboard.png")
    print("   └── dificil/dashboard.png")