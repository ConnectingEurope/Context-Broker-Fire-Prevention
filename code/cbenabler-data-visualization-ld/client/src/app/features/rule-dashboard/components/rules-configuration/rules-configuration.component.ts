import { Component, Input, Output, EventEmitter, ViewChildren, QueryList, OnInit,  } from '@angular/core';
import { RuleDashboardService } from '../../services/rule-dashboard.service';
import { BaseComponent } from  '../../../../shared/misc/base.component' //'src/app/shared/misc/base.component';
import { RuleEngineForm, RuleForm } from '../../models/rule-engine-form';
import { ConfirmationService } from 'primeng/api';
import { AccordionTab } from 'primeng/accordion/accordion';



@Component({
    selector: 'app-rules-configuration',
    templateUrl: './rules-configuration.component.html',
    styleUrls: ['./rules-configuration.component.scss'],
})
export class RulesConfigurationComponent extends BaseComponent implements OnInit {

    @Input() public re: RuleEngineForm;
    @Input() public rules: RuleForm[];
    
    @Output() public removeRuleEvent: EventEmitter<void> = new EventEmitter<void>();
    @Output() public favChange: EventEmitter<void> = new EventEmitter<void>();

    public accordionTabsSelected: boolean = false;

    @ViewChildren('accordionTab') private accordionTabs: QueryList<AccordionTab>;

    constructor(
        private ruleDashboardService: RuleDashboardService,
        private confirmationService: ConfirmationService,
    ) {
        super();
        
    }

    public ngOnInit(): void {
        
    }

    /*****************************************************************************
     Event functions
    *****************************************************************************/

    public onAddRule(): void {
        this.accordionTabsSelected = true;
        if (this.accordionTabs && this.accordionTabs.length > 0) {
            this.accordionTabs.forEach(a => a.selected = false);
        }
        this.rules.push({
            form: this.ruleDashboardService.createRuleForm(),
        });
    }

    public onRemoveRule(r: RuleForm, index: number): void {
        this.confirmationService.confirm({
            icon: 'pi pi-info',
            header: 'Are you sure you want to delete this rule?',
            message: 'The configuration of the rule "' + r.form.get("rule_name").value +
                '" will be deleted. Note that this change will only be confirmed when applying the configuration.',
            acceptLabel: 'Delete',
            rejectLabel: 'Cancel',
            accept: (): void => {
                this.removeRuleEvent.emit();
                const deleteid : Number = this.rules[index].form.get("id").value;
                if(deleteid.toString() !== ""){
                    console.log("DELETING ID ", deleteid)
                    this.ruleDashboardService.deleteRule(this.re.form.get("url").value, deleteid.toString());
                }
                this.rules.splice(index, 1);
            },
        });
    }

    public onFavChange(): void {
        this.favChange.emit();
    }



    
    /*****************************************************************************
     Accordion functions
    *****************************************************************************/

    private closeAccordionTabs(): void {
        setTimeout(() => {
            if (this.accordionTabs && this.accordionTabs.length > 0) {
                this.accordionTabs.forEach(a => a.selected = false);
            }
        });
    }

}
