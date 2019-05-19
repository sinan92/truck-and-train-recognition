export class History {
  camera_id: number;
  description: string;
  timestamp: string;
  wagon_id: string;

  constructor(camera_id: number, timestamp: string, wagon_id: string) {
    this.camera_id = camera_id;
    this.timestamp = timestamp;
    this.wagon_id = wagon_id;
  }
}
