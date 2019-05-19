import {Wagon} from './wagon';

export class Camera {
  camera_id: number;
  description: string;
  editable: boolean;
  connected: string;
  wagons: Wagon[];

  constructor(camera_id: number, description: string) {
    this.camera_id = camera_id;
    this.description = description;
    this.editable = false;
  }
}
