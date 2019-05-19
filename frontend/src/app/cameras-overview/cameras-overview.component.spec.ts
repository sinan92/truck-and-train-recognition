import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CamerasOverviewComponent } from './cameras-overview.component';

describe('CamerasOverviewComponent', () => {
  let component: CamerasOverviewComponent;
  let fixture: ComponentFixture<CamerasOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CamerasOverviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CamerasOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
