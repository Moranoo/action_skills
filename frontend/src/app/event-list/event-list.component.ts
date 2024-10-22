import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';  // Importer le service API

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.css']
})
export class EventListComponent implements OnInit {
  events: any[] = [];  // Variable pour stocker les événements

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    // Récupérer les événements depuis l'API
    this.apiService.getEvents().subscribe((data) => {
      this.events = data;  // Assigner les événements récupérés à la variable events
    });
  }
}
