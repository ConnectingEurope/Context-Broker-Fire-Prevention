import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RuleDashboardComponent } from './components/rule-dashboard.component';
import { RuleDashboardRoutingModule } from './rule-dashboard-routing.module';
import { AccordionModule } from 'primeng/accordion';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { BlockUIModule } from 'primeng/blockui';
import { TableModule } from 'primeng/table';
import { TreeModule } from 'primeng/tree';
import { CheckboxModule } from 'primeng/checkbox';
import { ScrollPanelModule } from 'primeng/scrollpanel';
import { TooltipModule } from 'primeng/tooltip';
import { MessageModule } from 'primeng/message';
import { SharedModule } from  '../../shared/shared.module' //'src/app/shared/shared.module';
import { RulesConfigurationComponent } from './components/rules-configuration/rules-configuration.component';
import { DropdownModule } from 'primeng/dropdown';
import { RuleFormComponent } from './components/rule-form/rule-form.component';


@NgModule({
    imports: [
        CommonModule,
        SharedModule,
        FormsModule,
        RuleDashboardRoutingModule,
        AccordionModule,
        DropdownModule,
        CardModule,
        ButtonModule,
        InputTextModule,
        ReactiveFormsModule,
        BlockUIModule,
        TableModule,
        TreeModule,
        CheckboxModule,
        ScrollPanelModule,
        TooltipModule,
        MessageModule,
    ],
    declarations: [
        RuleDashboardComponent,
        RulesConfigurationComponent,
        RuleFormComponent,
    ],
    providers: [],
})
export class RuleDashboardModule { }
