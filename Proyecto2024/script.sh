echo "Iniciando el frontend"
gnome-terminal -- bash -c "cd ./frontend/ && npm run dev; exec bash" &

echo "Iniciando el servidor de backend"
gnome-terminal -- bash -c "cd ./backend/ && python3 app.py; exec bash" &


