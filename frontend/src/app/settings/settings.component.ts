import { Component, OnInit } from '@angular/core';
import {CameraService} from '../services/camera.service';
import {WagonService} from '../services/wagon.service';
import {Camera} from '../models/camera';
import {MatSnackBar} from '@angular/material';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  title = 'Settings';
  cameras: Camera[] = [];
  wagon_id: number;

  constructor(private cameraService: CameraService, private wagonService: WagonService, private snackBar: MatSnackBar) { }

  ngOnInit() {
    this.cameraService.getAll().subscribe(cameras => this.cameras = cameras.filter(camera => camera.connected === 'true'));
  }

  enableEdit(id) {
    this.cameras.find(camera => camera.camera_id === id).editable = true;
  }

  save(id, description) {
    this.cameraService.saveCamera(id, description).subscribe();
    this.cameras.find(camera => camera.camera_id === id).editable = false;
  }

  addWagon() {
    this.wagonService.addExpectedWagon(this.wagon_id).subscribe(() => {
      this.snackBar.open('Wagon ' + this.wagon_id + ' has been added', 'Ok', {
        duration: 2000,
      });
      this.wagon_id = 0;
    });
  }

}
