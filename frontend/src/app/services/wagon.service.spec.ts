import { TestBed, inject } from '@angular/core/testing';

import { WagonService } from './wagon.service';
import {HttpClientModule} from '@angular/common/http';

describe('OrderService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WagonService],
      imports: [HttpClientModule]
    });
  });

  it('should be created', inject([WagonService], (service: WagonService) => {
    expect(service).toBeTruthy();
  }));
});
