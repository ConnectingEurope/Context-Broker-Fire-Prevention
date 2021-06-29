import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { HistoricalDashboardComponent } from './historical-dashboard.component';

describe('HistoricalDashboardComponent', () => {
  let component: HistoricalDashboardComponent;
  let fixture: ComponentFixture<HistoricalDashboardComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ HistoricalDashboardComponent ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HistoricalDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
