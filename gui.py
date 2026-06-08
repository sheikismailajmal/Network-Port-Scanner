import tkinter as tk
import socket
import csv

from scanner import scan_range
from service_detector import get_service
from database import get_scan_history
from banner_grabber import grab_banner


def start_scan():

    target = target_entry.get().strip()

    try:
        resolved_ip = socket.gethostbyname(target)

    except socket.gaierror:

        results_box.delete("1.0", tk.END)

        results_box.insert(
            tk.END,
            "Unable to resolve hostname."
        )

        return

    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())

    except ValueError:

        results_box.delete("1.0", tk.END)

        results_box.insert(
            tk.END,
            "Please enter valid port numbers."
        )

        return

    if start_port < 1 or end_port > 65535:

        results_box.delete("1.0", tk.END)

        results_box.insert(
            tk.END,
            "Ports must be between 1 and 65535."
        )

        return

    if start_port > end_port:

        results_box.delete("1.0", tk.END)

        results_box.insert(
            tk.END,
            "Start Port cannot be greater than End Port."
        )

        return

    status_label.config(text="Scanning...")
    window.update()

    results_box.delete("1.0", tk.END)

    results_box.insert(
        tk.END,
        f"Resolved IP: {resolved_ip}\n\n"
    )

    open_ports = scan_range(
        target,
        start_port,
        end_port
    )

    if not open_ports:

        results_box.insert(
            tk.END,
            "No open ports found.\n"
        )

        status_label.config(
            text="Scan Complete - No open ports found"
        )

        return

    for port in open_ports:

        service = get_service(port)

        banner = grab_banner(
            resolved_ip,
            port
        )

        results_box.insert(
            tk.END,
            f"Port {port} OPEN ({service})\n"
        )

        results_box.insert(
            tk.END,
            f"Banner: {banner}\n\n"
        )

    status_label.config(
        text=f"Scan Complete - {len(open_ports)} open port(s) found"
    )


def show_history():

    results_box.delete("1.0", tk.END)

    results_box.insert(
        tk.END,
        "===== SCAN HISTORY =====\n\n"
    )

    records = get_scan_history()

    if not records:

        results_box.insert(
            tk.END,
            "No scan history found."
        )

        return

    for record in records:

        results_box.insert(
            tk.END,
            f"ID:{record[0]} | "
            f"{record[1]} | "
            f"Port:{record[2]} | "
            f"{record[3]} | "
            f"{record[4]} | "
            f"{record[5]}\n"
        )


def clear_results():

    results_box.delete("1.0", tk.END)
    status_label.config(text="Ready")


def export_results():

    content = results_box.get(
        "1.0",
        tk.END
    ).strip()

    if not content:

        status_label.config(
            text="No results available to export"
        )

        return

    with open(
        "scan_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["Scan Results"])

        for line in content.splitlines():
            writer.writerow([line])

    status_label.config(
        text="Results exported to scan_results.csv"
    )


# MAIN WINDOW

window = tk.Tk()

window.title("Network Port Scanner")
window.geometry("650x600")


# TITLE

title_label = tk.Label(
    window,
    text="Network Port Scanner",
    font=("Arial", 16, "bold")
)

title_label.pack(pady=20)


# TARGET HOST

target_label = tk.Label(
    window,
    text="Target Host:"
)

target_label.pack()

target_entry = tk.Entry(
    window,
    width=40
)

target_entry.pack(pady=5)


# START PORT

start_port_label = tk.Label(
    window,
    text="Start Port:"
)

start_port_label.pack()

start_port_entry = tk.Entry(
    window,
    width=20
)

start_port_entry.pack(pady=5)


# END PORT

end_port_label = tk.Label(
    window,
    text="End Port:"
)

end_port_label.pack()

end_port_entry = tk.Entry(
    window,
    width=20
)

end_port_entry.pack(pady=5)


# BUTTONS

scan_button = tk.Button(
    window,
    text="Start Scan",
    command=start_scan
)

scan_button.pack(pady=10)

history_button = tk.Button(
    window,
    text="View History",
    command=show_history
)

history_button.pack(pady=5)

export_button = tk.Button(
    window,
    text="Export CSV",
    command=export_results
)

export_button.pack(pady=5)

clear_button = tk.Button(
    window,
    text="Clear Results",
    command=clear_results
)

clear_button.pack(pady=5)


# RESULTS LABEL

results_label = tk.Label(
    window,
    text="Results:"
)

results_label.pack()


# RESULTS AREA

results_frame = tk.Frame(window)
results_frame.pack(pady=10)

scrollbar = tk.Scrollbar(results_frame)

results_box = tk.Text(
    results_frame,
    height=10,
    width=70,
    yscrollcommand=scrollbar.set
)

scrollbar.config(
    command=results_box.yview
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

results_box.pack(
    side=tk.LEFT
)


# STATUS BAR

status_label = tk.Label(
    window,
    text="Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W
)

status_label.pack(
    side=tk.BOTTOM,
    fill=tk.X
)

window.mainloop()