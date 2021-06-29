import { Component, OnInit } from '@angular/core';
import { User} from '../../shared/models/user';
import { FormGroup,FormControl, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { LoginService } from '../../shared/services/login.service';
import { timeoutWith } from 'rxjs/operators';
import { Md5 } from 'ts-md5/dist/md5';
@Component({
  selector: 'app-signup-page',
  templateUrl: './signup-page.component.html',
  styleUrls: ['./signup-page.component.scss']
})
export class SignupPageComponent implements OnInit {

  successAlert:boolean = false;
  errorAlert:boolean = false;

  registerForm = this.fb.group({
    email: ['', Validators.required],
    username:  ['', Validators.required],
    name:  ['', Validators.required],
    password:['',Validators.required],
    secondPassword:  ['', Validators.required]
  });
  constructor(private fb: FormBuilder, private loginService: LoginService) { }

  ngOnInit(): void {
  }

  onSubmit(){
   this.errorAlert = false;
   this.successAlert = false;
    if(this.registerForm.valid){
      if(this.registerForm.value.password ===  this.registerForm.value.secondPassword){
            const user: User = {
            email : this.registerForm.value.email,
            username: this.registerForm.value.username,
            name: this.registerForm.value.name,
            password: Md5.hashStr(this.registerForm.value.password)
          } 
              
        this.loginService.register(user).toPromise().then(id =>{
          
          this.successAlert = true;
        });
      }else{
        this.errorAlert = true;
      }
    }


  }
}
