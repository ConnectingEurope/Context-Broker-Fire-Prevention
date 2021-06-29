import { Component, OnInit } from '@angular/core';
import { User} from '../../shared/models/user';
import { FormGroup,FormControl, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { LoginService } from '../../shared/services/login.service';
import { Router } from '@angular/router';
import { Md5 } from 'ts-md5/dist/md5';

@Component({
  selector: 'app-signin-page',
  templateUrl: './signin-page.component.html',
  styleUrls: ['./signin-page.component.scss']
})
export class SigninPageComponent implements OnInit {

  errorAlert: boolean = false;
  errorMessage: string = '';
  loginForm = this.fb.group({
    email: ['', Validators.required],
    password:['',Validators.required],
  });
  constructor(private fb: FormBuilder, private loginService: LoginService, private router: Router) { }

  ngOnInit(): void {
  }
  onSubmit(){
   
    if(this.loginForm.valid){
      const user: User = {
        email : this.loginForm.value.email,
        password :Md5.hashStr(this.loginForm.value.password)
      } 
      this.loginService.login(user).toPromise().then(userData =>{
        sessionStorage.setItem('logged', 'true');
        sessionStorage.setItem('userData', JSON.stringify(userData));
        this.router.navigate(["/"]).then(() => {
          window.location.reload();
        });
      }, error =>{
        this.errorAlert = true;
        this.errorMessage = error['error']['Exception'];
      });
    }


  }

}
