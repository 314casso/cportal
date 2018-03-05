import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {
  MatButtonModule,
  MatInputModule,
  MatMenuModule,
  MatToolbarModule,
  MatSidenavModule,
  MatListModule,
  MatIconModule,
  MatTableModule,
  MatPaginatorModule,
  MatSortModule,
  MatCardModule
} from '@angular/material';

@NgModule({
  imports: [CommonModule],
  exports: [
    MatButtonModule,
    MatInputModule,
    MatMenuModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatIconModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatCardModule
  ]
})
export class MaterialModule {}
