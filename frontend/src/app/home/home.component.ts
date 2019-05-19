import {Component, OnInit, ViewChild, ViewEncapsulation} from '@angular/core';
import {WagonService} from '../services/wagon.service';
import {Wagon} from '../models/wagon';
import {ErrorStateMatcher, MatPaginator, MatTableDataSource} from '@angular/material';
import {FormControl, FormGroup, FormGroupDirective, NgForm, Validators} from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})

export class HomeComponent implements OnInit {
  title = 'Wagon tracing';
  lat = 50.935207;
  lng = 5.509369;
  markers: Wagon[] = [];
  editMode = false;
  wagonNumberValue: number;
  displayedColumns: string[] = ['id', 'timestamp', 'lat', 'lang', 'delete'];
  dataSource: MatTableDataSource<Wagon>;
  markerForm = new FormGroup({
    wagonNumberValidator: new FormControl('', [Validators.max(999999999999), Validators.pattern('^[0-9]*$')])
  });

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(private wagonService: WagonService) {  }

  matcher = new MyErrorStateMatcher();

  ngOnInit() {
    this.wagonService.getAll().subscribe((wagons) => {
      for (const wagon of wagons) {
        this.markers.push(wagon);
      }
      this.dataSource = new MatTableDataSource<Wagon>(this.markers);
      this.dataSource.paginator = this.paginator;
    });
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
    this.markers = this.dataSource.filteredData;
  }

  checkEditable() {
    this.editMode = false;
    this.markers.forEach(marker => {
      if (marker.edit === true) {
        this.editMode = true;
      }
    });
  }

  placeMarker($event) {
    this.checkEditable();
    if (this.editMode) {
      alert('You can\'t add a wagon spot without finishing the current one first.');
    } else {
      this.resetMarkers();
      this.markers.push(new Wagon(0, $event.coords.lng, $event.coords.lat, 0, true, false));
      this.checkEditable();
    }
  }

  addClicked() {
    this.markers.forEach((marker, index) => {
      if (marker.edit === true) {
        this.markers[index].wagon_id = this.wagonNumberValue;
        this.markers[index].edit = false;
        this.wagonService.addWagon(marker.wagon_id, marker.longitude, marker.latitude).subscribe();
        this.refreshTable();
      }
    });
    this.checkEditable();
  }

  refreshTable() {
    this.dataSource = new MatTableDataSource<Wagon>(this.markers);
  }

  deleteClicked() {
    this.markers.forEach((marker, index) => {
      if (marker.edit === true) {
        this.markers.splice(index, 1);
      }
    });
    this.checkEditable();
  }

  deleteMarkerClicked(id) {
    this.wagonService.deleteWagon(id).subscribe(() => {
      this.markers = this.markers.filter(marker => marker.wagon_id !== id);
      this.refreshTable();
    }); // Delete from DB
  }

  tableRowClicked(id) {
    this.resetMarkers();
    this.markers.find(marker => marker.wagon_id === id).clicked = true;
    this.markers.find(marker => marker.wagon_id === id).zIndex = 100;
  }

  resetMarkers() {
    this.markers.filter(marker => marker.clicked === true).forEach(marker => {
      marker.clicked = false;
      marker.zIndex = 0;
    });
  }
}

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}
