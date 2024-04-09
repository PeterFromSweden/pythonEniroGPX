import os.path
import sys
import gpxpy.gpx
import filename

def main(file_path):
    try:
        gpx_file = open(file_path, 'r', encoding='utf-8')

    except IOError as e:
        print(f'Error {e}')
        return
    #gpx_path = os.path.dirname(file_path)
    gpx_path = os.path.curdir
    gpx = gpxpy.parse(gpx_file)
    for route in gpx.routes:
        route_name = route.name
        # The following was necessary when file was open without encoding...
        # route_name = route.name.replace('…', '')
        # route_name = route_name.encode("latin1").decode('utf-8')
        route_name = filename.make_valid(route_name)
        route_path = os.path.join(gpx_path, route_name + '.gpx')
        try:
            route_file = open(route_path, 'r')
            gpx_route = gpxpy.parse(route_file)
            if route == gpx_route.routes[1]:
                raise IOError
        except (FileNotFoundError, IOError) as e:
            route_gpx = gpxpy.gpx.GPX()
            route_gpx.routes.append(route)
            route_file = open(route_path, 'w', encoding='utf-8')
            route_file.write(route_gpx.to_xml())
        except IndexError:
            pass


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(os.path.join(
            os.path.dirname(sys.argv[0]), 'test', 'Eniro-Nautical_20240405-142553.gpx'))
