import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ResultService } from 'src/app/services/result.service';


@Component({
  selector: 'app-live',
  templateUrl: './live.component.html',
  styleUrls: ['./live.component.scss']
})
export class LiveComponent implements OnInit {

  serverAlive = false;

  constructor(private http: HttpClient, private resultService: ResultService) {
    this.resultService.isAlive().subscribe(data => console.log(data));
  }

  ngOnInit() {
  }

}
