import { TestBed, ComponentFixture } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RulesConfigurationComponent } from './rules-configuration.component';
import { RuleDashboardModule } from '../../rule-dashboard.module';
import { AppMessageService } from '../../../../shared/services/app-message-service' //'src/app/shared/services/app-message-service';
import { ConfirmationService } from 'primeng/api';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('ServiceConfigurationComponent', () => {

    let fixture: ComponentFixture<RulesConfigurationComponent>;
    let component: RulesConfigurationComponent;

    beforeEach(() => {
        const appMessageServiceSpyObj: any = jasmine.createSpyObj('AppMessageService', ['add']);
        const confirmationServiceSpyObj: any = jasmine.createSpyObj('ConfirmationService', ['confirm']);

        TestBed.configureTestingModule({
            imports:
                [
                    RuleDashboardModule,
                    HttpClientTestingModule,
                    BrowserAnimationsModule,
                ],
            providers: [
                { provide: AppMessageService, useValue: appMessageServiceSpyObj },
                { provide: ConfirmationService, useValue: confirmationServiceSpyObj },
            ],
        });

        fixture = TestBed.createComponent(RulesConfigurationComponent);
        component = fixture.debugElement.componentInstance;
    });

    it('setup', () => {
        expect(component).toBeTruthy();
    });

});
