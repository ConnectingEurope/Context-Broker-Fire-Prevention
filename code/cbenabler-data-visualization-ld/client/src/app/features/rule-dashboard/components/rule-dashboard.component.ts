import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { RuleDashboardService } from '../services/rule-dashboard.service'
import { RuleEngineForm, RuleForm } from '../models/rule-engine-form'
import { takeUntil } from 'rxjs/operators';
import { BaseComponent } from '../../../shared/misc/base.component';
import { AppMessageService } from '../../../shared/services/app-message-service'//'src/app/shared/services/app-message-service';
import { RuleEngineConfiguration, RulesConfiguration } from '../models/rule-engine-configuration';
import { RulesConfigurationComponent } from './rules-configuration/rules-configuration.component';
import { InputWithValidationComponent } from '../../../shared/templates/input-with-validation/input-with-validation.component';



@Component({
  selector: 'app-rule-dashboard',
  templateUrl: './rule-dashboard.component.html',
  styleUrls: ['./rule-dashboard.component.scss']
})
export class RuleDashboardComponent extends BaseComponent implements OnInit {

  public configurationLoaded: boolean = false;
  public accordionTabsSelected: boolean = false;
  public ruleEngine: RuleEngineForm;
  public rules: RuleForm[] = [];

  @ViewChild('rulesConfiguration') private rulesConfiguration: RulesConfigurationComponent;
  @ViewChild('urlInput') private urlInput: InputWithValidationComponent;

  constructor(
    private router: Router,
    private ruleDashboardService: RuleDashboardService,
    private appMessageService: AppMessageService,
  ) {
      super();
      
   }

  ngOnInit(): void {
    this.ruleEngine = {
        form: this.ruleDashboardService.createRuleEngineForm()
    }
    this.getRulesConfiguration();
  }


  /*****************************************************************************
     Event functions
    *****************************************************************************/


    public onApplyConfiguration(): void {
        this.applyConfiguration();
    }
    
    public onUrlChange(): void {
        if (this.rulesConfiguration) {
            this.rules = [];
        }
    }

    
    public onCheckRuleEngine(): void {
        const url: string = this.ruleEngine.form.value.url;
        this.ruleDashboardService.checkRuleEngineHealth(url).pipe(takeUntil(this.destroy$)).subscribe(
            isLive => {
                isLive.length !== null ? this.onCheckRuleEngineSuccess() : this.onCheckRuleEngineFail(false);

            },
            err => {
                this.onCheckRuleEngineFail(err);
            },
            () => {
                this.rules = [];
                this.getRulesConfiguration()});
    }

    private onCheckRuleEngineSuccess(): void {
        this.urlInput.showInfo();
    }

    private onCheckRuleEngineFail(err: boolean): void {

        this.urlInput.showWarning();
    }

    /*****************************************************************************
     Getting configuration functions
    *****************************************************************************/


  private getRulesConfiguration(): void {
      this.ruleDashboardService.getRules(this.ruleEngine.form.get("url").value).pipe(takeUntil(this.destroy$)).subscribe(
          rules => {
              rules.forEach(r => {this.rules.push({
                form : this.ruleDashboardService.createRuleFormFromConfig(r),
              })})
          },
          err => {
            this.appMessageService.add({ severity: 'error', summary: 'Something went wrong loading the rules' });
          },
          () => {this.configurationLoaded = true;}
      )
  }

  /*****************************************************************************
     Setting configuration functions
    *****************************************************************************/

     private applyConfiguration(): void {
        const config: RuleEngineConfiguration = this.getRuleEngine();
        const rules: RulesConfiguration[] = this.getRules()
        this.ruleDashboardService.postRules(this.ruleEngine.form.get("url").value, rules).pipe(takeUntil(this.destroy$)).subscribe(
            res => {
                this.onApplyConfigurationSuccess();
            },
            err => {
                this.onApplyConfigurationFail();
            },
            ()=> {
                this.rules = [];
                this.getRulesConfiguration();
            });
    }

    private onApplyConfigurationSuccess(): void {
        this.appMessageService.add({ severity: 'success', summary: 'Configuration applied' });
        this.router.navigate(['/rule-engine'])
    }

    private onApplyConfigurationFail(): void {
        this.appMessageService.add({ severity: 'error', summary: 'Something went wrong applying the configuration' });
    }

    private getRuleEngine(): RuleEngineConfiguration {
        
        return {
            url: this.ruleEngine.form.get('url').value,
            rules: this.getRules(),
        };
    }

    private getRules(): RulesConfiguration[] {
        return this.rules.map(r => {
            return {
                rule_name: r.form.get('rule_name').value,
                service_name: r.form.get('service_name').value,
                value_category: r.form.get('value_category').value,
                value_subcategory: r.form.get('value_subcategory').value,
                value_severity: r.form.get('value_severity').value,
                operator: r.form.get('operator').value,
                attribute_name: r.form.get('attribute_name').value,
                threshold: r.form.get('threshold').value,
                id: r.form.get('id').value,
                entity_type: r.form.get('entity_type').value,
                subscription_id: r.form.get('subscription_id').value,
                recurrence_seconds: r.form.get('recurrence_seconds').value,
            };
        });
    }
      /*****************************************************************************
     Validation functions
    *****************************************************************************/

    
}
