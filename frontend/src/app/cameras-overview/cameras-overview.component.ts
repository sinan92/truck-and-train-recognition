import {Component, OnDestroy, OnInit} from '@angular/core';
import {MatTreeFlatDataSource, MatTreeFlattener} from '@angular/material';
import {FlatTreeControl} from '@angular/cdk/tree';
import {CameraService} from '../services/camera.service';
import {Camera} from '../models/camera';
import {Observable} from 'rxjs';
import {HistoryService} from '../services/history.service';

@Component({
  selector: 'app-cameras-overview',
  templateUrl: './cameras-overview.component.html',
  styleUrls: ['./cameras-overview.component.css'],
})
export class CamerasOverviewComponent implements OnInit, OnDestroy {
  title = 'Cameras overview';
  cameras: Camera[] = [];
  interval;
  histories: History[] = [];

  constructor(private cameraService: CameraService, private historyService: HistoryService) {}

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 1000);

  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.cameraService.getAll().subscribe(cameras => {
      this.cameras = cameras.filter(camera => camera.connected === 'true');
    });
    this.historyService.getAll().subscribe(histories => this.histories = histories);
  }

}
