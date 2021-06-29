import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { ConfirmationService } from 'primeng/api';
import { SelectItem } from 'primeng/api/selectitem';
import { takeUntil } from 'rxjs/operators';
import { BaseComponent } from '../../../../shared/misc/base.component';
import { AppMessageService } from '../../../../shared/services/app-message-service';
import { RuleEngineForm, RuleForm } from '../../models/rule-engine-form';
import { RuleDashboardService } from '../../services/rule-dashboard.service';

@Component({
  selector: 'app-rule-form',
  templateUrl: './rule-form.component.html',
  styleUrls: ['./rule-form.component.scss']
})
export class RuleFormComponent extends BaseComponent implements OnInit {

  @Input() public rule: RuleForm;
  @Input() public re: RuleEngineForm;

    public categoriesAvailable: boolean = false;
    public subcategoriesAvailable: boolean = false;
    public severityAvailable: boolean = false;
    public attributesAvailable: boolean = false;

    public selectCategories: SelectItem[] = [];
    public selectSubcategories: SelectItem[] = [];

    public operators: SelectItem[] = [
        { label: '>', value: 'greater' },
        { label: '==', value: 'equal' },
        { label: '<', value: 'lower' },
    ];

    public severities: SelectItem[] = [];
    public attributes: SelectItem[] = [];

  constructor(
    private ruleDashboardService: RuleDashboardService,
    private appMessageService: AppMessageService,
    ) {
      super();
    }

  ngOnInit(): void {
    this.getCategories();
    this.getSeverities();
    if(this.rule.form.get('service_name').value !== ""){
      this.getAttributes();
    }
  }
  public onChangeCategory(): void{
    this.selectSubcategories= [];
    this,this.getSubcategories(this.rule.form.get('value_category').value);
  }

  public onChange(): void {

  }


    /*****************************************************************************
     DropDown Lists
    *****************************************************************************/
     
  private getCategories(): void {
    //this.ruleDashboardService.getCategories().pipe(takeUntil(this.destroy$)).toPromise().then(data => this.loadCategories(data));   /*
    this.ruleDashboardService.getCategories(this.re.form.get("url").value).pipe(takeUntil(this.destroy$)).subscribe(
        categories => {
            this.loadCategories(categories);
        },
        err => {
            this.appMessageService.add({severity: 'error', summary: 'Something went wrong loading the categories'});
        },
        () => {
          this.categoriesAvailable=true;
          if(this.rule.form.get("value_category").value != "") {
              this.getSubcategories(this.rule.form.get('value_category').value);
          }
          
        }
    )
      
  }
  private loadCategories(categories: string[]) : void{
      categories.forEach(c => {
          this.selectCategories.push({
              label: c,
              value: c,
          });
          //this.getSubcategories(c)
      }
      );
  }

  private getSubcategories(category : string): void {
      this.ruleDashboardService.getSubCategories(this.re.form.get("url").value, category).pipe(takeUntil(this.destroy$)).subscribe(
          subcategories => {
              this.loadSubcategories(subcategories);
          },
          err => {
              this.appMessageService.add({severity: 'error', summary: 'Something went wrong loading the subcategories'});
          },
          () => {
            this.subcategoriesAvailable=true;
          }

      )
  }

  private loadSubcategories(subcategories : string[]): void {
      subcategories.forEach(s => this.selectSubcategories.push({
          label: s,
          value: s
      }));
  }

  private getSeverities(): void {
    this.ruleDashboardService.getSeverityLevels(this.re.form.get("url").value).pipe(takeUntil(this.destroy$)).subscribe(
      severityLevels =>{
        this.loadSeverities(severityLevels);
      },
      err => {
        this.appMessageService.add({severity: 'error', summary: 'Something went wrong loading the severity levels'});
      },
      () => {
        this.severityAvailable=true;
      }
    )
  }

  private loadSeverities(severityLevels: string[]): void {
    severityLevels.forEach(s => this.severities.push({
      label: s,
      value: s,
    }) )
  }

  private getAttributes(): void {
    this.ruleDashboardService.getAttributes(this.re.form.get("url").value, this.rule.form.get("service_name").value).pipe(takeUntil(this.destroy$)).subscribe(
      attributes =>{
        this.loadAttributes(attributes);
        
      },
      err => {
        this.attributesAvailable=false;
        this.appMessageService.add({severity: 'error', summary: 'Something went wrong loading the attributes'});
      },
      () => {this.attributesAvailable=true;}
    )
  }
  private loadAttributes(attributes: string[]) {
    attributes.forEach(a => this.attributes.push({
      label: a,
      value: a,
    }))
  }

  public onCheckService() :void {
    this.attributes = []
    this.attributesAvailable=false;
    this.getAttributes();
  }

}

