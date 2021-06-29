export interface RuleEngineConfiguration {
    url: string;
    rules: RulesConfiguration[];
}

export interface RulesConfiguration {
    id: number;
    rule_name: string;
    service_name: string;
    entity_type: string;
    attribute_name: string;
    operator: string;
    threshold: number;
    value_category: string;
    value_subcategory: string;
    value_severity: string;
    subscription_id: string;
    recurrence_seconds: number;
    
    
}

export interface CategoryConfiguartion{
    id: number;
    name: string;
    //subcategories: SubcategoryConfiguration[];
}

export interface SubcategoryConfiguration{
    subcategory: string;
}
