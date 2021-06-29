
import { TestBed, ComponentFixture } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RuleDashboardModule } from '../../rule-dashboard.module';
import { RuleFormComponent } from './rule-form.component';

describe('SubscriptionsDialogComponent', () => {

    let fixture: ComponentFixture<RuleFormComponent>;
    let component: RuleFormComponent;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports:
                [
                    RuleDashboardModule,
                    HttpClientTestingModule,
                ],
        });

        fixture = TestBed.createComponent(RuleFormComponent);
        component = fixture.debugElement.componentInstance;
    });

    it('setup', () => {
        expect(component).toBeTruthy();
    });

});