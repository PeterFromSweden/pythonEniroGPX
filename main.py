import os
import shutil
from datetime import datetime

import gpxpy.gpx
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# path_to_watch = r'C:\Users\Peter\Dropbox\Båt\GPS'  # Dropbox style
# path_to_watch = r'C:\Users\Peter\OneDrive\Båt\GPS'  # Onedrive style
path_to_watch = r'G:\Min enhet\Båt\GPS'  # Google Drive style


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created':
            print(f"Received created event: {event.src_path}")
            create_delta_gpx(event.src_path)
        # elif event.event_type == 'modified':
        #    print(f"Received modified event: {event.src_path}")


def create_delta_gpx(file_path):
    file_name = os.path.basename(file_path)
    print(f'New file: {file_name}')
    if not file_name.startswith('Eniro-Nautical_'):
        print(f'Skipped!')
        return

    # Read last delta to find which was last file processed
    delta = True
    try:
        gpx_file = open(os.path.join(path_to_watch, 'Eniro-Delta.gpx'), 'r')
    except IOError as e:
        # No delta => no previous file
        delta = False

    if delta:
        delta_gpx = gpxpy.parse(gpx_file)
        # Read last file
        last_file_name = delta_gpx.name
        last_datetime_string = last_file_name[15:]
        last_file_path = os.path.join(path_to_watch, last_file_name)
        print(f'Last file: {last_file_name}')
        gpx_file = open(last_file_path, 'r')
        last_gpx = gpxpy.parse(gpx_file)
    else:
        last_gpx = gpxpy.gpx.GPX()

    delta_gpx = gpxpy.gpx.GPX()
    delta_gpx.name = file_name  # To be used as last file processed next time

    # Read current file
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)

    # List all routes from last file
    old_route_names = list(map(lambda obj: obj.name, last_gpx.routes))

    for route in gpx.routes:
        if route.name not in old_route_names:
            print(f'New route: {route.name}')
            delta_gpx.routes.append(route)

    # Store all new routes in delta, preserve the previous delta with date for curiosity
    if delta:
        shutil.copyfile(os.path.join(path_to_watch, 'Eniro-Delta.gpx'),
                        os.path.join(path_to_watch, f'Eniro-OldDelta_{last_datetime_string}'))

    gpx_file = open(os.path.join(path_to_watch, 'Eniro-Delta.gpx'), 'w')
    gpx_file.write(delta_gpx.to_xml())


if __name__ == '__main__':
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()
    print(f'Monitoring {path_to_watch}')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

