import { TestBed, ComponentFixture } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { RuleDashboardComponent } from './rule-dashboard.component';
import { RuleDashboardModule } from '../rule-dashboard.module';
import { AppMessageService } from '../../../shared/services/app-message-service'//'src/app/shared/services/app-message-service';
import { ConfirmationService } from 'primeng/api';

describe('RuleDashboardComponent', () => {
  let component: RuleDashboardComponent;
  let fixture: ComponentFixture<RuleDashboardComponent>;

  beforeEach(() => {
    const appMessageServiceSpyObj: any = jasmine.createSpyObj('AppMessageService', ['add']);
    const confirmationServiceSpyObj: any = jasmine.createSpyObj('ConfirmationService', ['confirm']);

    TestBed.configureTestingModule({
        imports:
            [
                RuleDashboardModule,
                HttpClientTestingModule,
                RouterTestingModule,
            ],
        providers: [
            { provide: AppMessageService, useValue: appMessageServiceSpyObj },
            { provide: ConfirmationService, useValue: confirmationServiceSpyObj },
        ],
    });

    fixture = TestBed.createComponent(RuleDashboardComponent);
    component = fixture.debugElement.componentInstance;
});

it('setup', () => {
    expect(component).toBeTruthy();
});

});
