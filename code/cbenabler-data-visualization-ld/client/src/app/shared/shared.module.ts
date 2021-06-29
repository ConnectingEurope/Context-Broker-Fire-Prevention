import { NgModule, ModuleWithProviders } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { AccordionModule } from 'primeng/accordion';
import { AccordionTabHeaderComponent } from './templates/accordion-tab-header/accordion-tab-header.component';
import { JsonDialogComponent } from './templates/json-dialog/json-dialog.component';
import { DialogModule } from 'primeng/dialog';
import { ClipboardModule } from 'ngx-clipboard';
import { DropdownModule } from 'primeng/dropdown';
import { TooltipModule } from 'primeng/tooltip';
import { InputWithValidationComponent } from './templates/input-with-validation/input-with-validation.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
    declarations: [
        AccordionTabHeaderComponent,
        JsonDialogComponent,
        InputWithValidationComponent,
    ],
    imports: [
        CommonModule,
        ButtonModule,
        TableModule,
        AccordionModule,
        DialogModule,
        ClipboardModule,
        DropdownModule,
        FormsModule,
        ReactiveFormsModule,
        TooltipModule,
    ],
    exports: [
        CommonModule,
        ButtonModule,
        TableModule,
        AccordionModule,
        DialogModule,
        ClipboardModule,
        AccordionTabHeaderComponent,
        JsonDialogComponent,
        InputWithValidationComponent,
    ],
})
export class SharedModule {
    public static forRoot(): ModuleWithProviders<SharedModule> {
        return {
            ngModule: SharedModule,
            providers: [],
        };
    }
}
