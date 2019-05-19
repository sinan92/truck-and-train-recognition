export class Wagon {
  wagon_id: number;
  last_timestamp: string;
  longitude: number;
  latitude: number;
  last_camera: number;
  edit: boolean;
  clicked: boolean;
  zIndex: number;

  constructor(wagon_id: number, longitude: number, latitude: number, last_camera: number, edit: boolean, clicked: boolean) {
    this.wagon_id = wagon_id;
    this.longitude = longitude;
    this.latitude = latitude;
    this.last_camera = last_camera;
    this.edit = edit;
    this.clicked = clicked;
    this.zIndex = 0;
  }
}
