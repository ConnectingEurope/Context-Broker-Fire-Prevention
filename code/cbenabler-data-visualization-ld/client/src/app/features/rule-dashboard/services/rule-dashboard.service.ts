import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Utils } from '../../../shared/misc/utils'//'src/app/shared/misc/utils';
import { RuleEngineConfiguration, RulesConfiguration } from '../models/rule-engine-configuration';

@Injectable({
    providedIn: 'root',
})

export class RuleDashboardService {

    public defaultRuleEngineName: string = 'New Rule Engine';
    public defaultRuleHeader: string = 'New Rule';
    public ruleEngineHeaderWhenEmpty: string = 'Rule Engine without name';
    public ruleHeaderWhenEmpty: string = 'No rule specified';


    constructor(
        private http: HttpClient,
    ) { }

    public createRuleEngineForm(): FormGroup {
        return new FormGroup({
            url: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
        });
    }

    public createRuleForm(): FormGroup {
        return new FormGroup({
            rule_name: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            service_name: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            value_category: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            value_subcategory: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            value_severity: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            attribute_name: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            operator: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            threshold: new FormControl('', [Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            recurrence_seconds: new FormControl('',[Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            id: new FormControl('',[Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            entity_type: new FormControl('',[Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),
            subscription_id: new FormControl('',[Validators.required, Validators.pattern(Utils.whiteSpaceExp)]),            
        });
    }

    public createRuleFormFromConfig(rConfig: RulesConfiguration): FormGroup {
        const formGroup: FormGroup = this.createRuleForm();
        formGroup.get('rule_name').setValue(rConfig.rule_name);
        formGroup.get('service_name').setValue(rConfig.service_name);
        formGroup.get('value_category').setValue(rConfig.value_category);
        formGroup.get('value_subcategory').setValue(rConfig.value_subcategory);
        formGroup.get('value_severity').setValue(rConfig.value_severity);
        formGroup.get('attribute_name').setValue(rConfig.attribute_name);
        formGroup.get('operator').setValue(rConfig.operator);
        formGroup.get('threshold').setValue(rConfig.threshold);
        formGroup.get('recurrence_seconds').setValue(rConfig.recurrence_seconds);
        formGroup.get('id').setValue(rConfig.id);
        formGroup.get('subscription_id').setValue(rConfig.subscription_id);
        formGroup.get('entity_type').setValue(rConfig.entity_type);
        return formGroup;
    }

    public checkRuleEngineHealth(url: string): Observable<string> {
        return this.checkHealth(url, "api/health")
        //return this.http.get<string>(url+"/health");
    }

    public postRules(url: string, rules: RulesConfiguration[]): Observable<void> {
        return this.http.post<void>("/api/rule-engine", rules);
    }

    public deleteRule(url: string, id: string) {
        return this.http.delete("/api/rule-engine/"+id).subscribe(()=> {console.log("Delete success")});
    }

    public getCategories(url:string): Observable<string[]> {
        return this.http.get<string[]>("/api/categories");
    }

    public getSubCategories(url:string, category:string): Observable<string[]> {
        return this.http.get<string[]>("/api/subcategories/"+category);
    }

    public getSeverityLevels(url:string): Observable<string[]> {
        console.log("GET ", this.http.get<string[]>("/api/severity"))
        return this.http.get<string[]>("/api/severity");
    }

    public getRules(url:string): Observable<RulesConfiguration[]>{
        console.log("WORKING")
        return this.http.get<RulesConfiguration[]>("/api/rule-engine");
    }

    public getAttributes(url: string, service: string): Observable<string[]> {
        return this.http.get<string[]>("/api/attributes/"+service);
    }
    
    private checkHealth(url: string, api: string): Observable<string> {
        let parameters: HttpParams = new HttpParams();
        parameters = parameters.append('url', url);

        return this.http.get<string>(api, { params: parameters });
    }
}
