/* ===== Data ===== */
const patients = [
  { id: 'P001', name: 'Aminata Diallo', dob: '1985-03-12', phone: '+221 77 123 4567', doctor: 'Dr. Kouyaté', status: 'Actif' },
  { id: 'P002', name: 'Mamadou Traoré', dob: '1970-08-25', phone: '+221 76 234 5678', doctor: 'Dr. Mbaye', status: 'En traitement' },
  { id: 'P003', name: 'Fatou Sow', dob: '1992-11-05', phone: '+221 70 345 6789', doctor: 'Dr. Kouyaté', status: 'Actif' },
  { id: 'P004', name: 'Ibrahima Bah', dob: '1960-01-30', phone: '+221 78 456 7890', doctor: 'Dr. Dieng', status: 'Sorti' },
  { id: 'P005', name: 'Kadiatou Camara', dob: '1998-06-14', phone: '+221 77 567 8901', doctor: 'Dr. Mbaye', status: 'Actif' },
  { id: 'P006', name: 'Oumar Coulibaly', dob: '1975-09-22', phone: '+221 76 678 9012', doctor: 'Dr. Dieng', status: 'En traitement' },
  { id: 'P007', name: 'Aissatou Barry', dob: '2001-04-18', phone: '+221 70 789 0123', doctor: 'Dr. Kouyaté', status: 'Actif' },
];

const appointments = [
  { patient: 'Aminata Diallo', doctor: 'Dr. Kouyaté', date: '2026-04-05', time: '08:30', reason: 'Consultation générale', status: 'Confirmé' },
  { patient: 'Mamadou Traoré', doctor: 'Dr. Mbaye', date: '2026-04-05', time: '09:00', reason: 'Suivi cardiologique', status: 'En attente' },
  { patient: 'Fatou Sow', doctor: 'Dr. Kouyaté', date: '2026-04-05', time: '10:30', reason: 'Bilan sanguin', status: 'Confirmé' },
  { patient: 'Ibrahima Bah', doctor: 'Dr. Dieng', date: '2026-04-06', time: '14:00', reason: 'Radiologie', status: 'Confirmé' },
  { patient: 'Kadiatou Camara', doctor: 'Dr. Mbaye', date: '2026-04-07', time: '11:00', reason: 'Vaccination', status: 'En attente' },
  { patient: 'Oumar Coulibaly', doctor: 'Dr. Dieng', date: '2026-04-07', time: '15:30', reason: 'Consultation générale', status: 'Annulé' },
];

const doctors = [
  { name: 'Dr. Kouyaté', specialty: 'Médecine générale', patients: 45, experience: '12 ans', available: true },
  { name: 'Dr. Mbaye', specialty: 'Cardiologie', patients: 30, experience: '8 ans', available: true },
  { name: 'Dr. Dieng', specialty: 'Radiologie', patients: 22, experience: '15 ans', available: false },
  { name: 'Dr. Baldé', specialty: 'Pédiatrie', patients: 38, experience: '6 ans', available: true },
  { name: 'Dr. Touré', specialty: 'Chirurgie', patients: 18, experience: '20 ans', available: true },
  { name: 'Dr. Condé', specialty: 'Gynécologie', patients: 27, experience: '10 ans', available: false },
];

const admissions = [
  { month: 'Oct', count: 18 },
  { month: 'Nov', count: 22 },
  { month: 'Déc', count: 15 },
  { month: 'Jan', count: 28 },
  { month: 'Fév', count: 20 },
  { month: 'Mar', count: 31 },
];

const specialties = [
  { label: 'Méd. générale', pct: 35, color: '#2563eb' },
  { label: 'Cardiologie',   pct: 22, color: '#7c3aed' },
  { label: 'Pédiatrie',     pct: 18, color: '#16a34a' },
  { label: 'Radiologie',    pct: 14, color: '#d97706' },
  { label: 'Autres',        pct: 11, color: '#dc2626' },
];

/* ===== Helpers ===== */
function statusBadge(status) {
  const map = {
    'Actif': 'badge-success',
    'En traitement': 'badge-warning',
    'Sorti': 'badge-primary',
    'Confirmé': 'badge-success',
    'En attente': 'badge-warning',
    'Annulé': 'badge-danger',
  };
  return `<span class="badge ${map[status] || 'badge-primary'}">${status}</span>`;
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

function initials(name) {
  return name.replace('Dr. ', '').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

/* ===== Render functions ===== */
function renderRecentPatients() {
  const tbody = document.getElementById('recent-patients-table');
  tbody.innerHTML = patients.slice(0, 5).map(p => `
    <tr>
      <td><strong>${p.name}</strong></td>
      <td>${new Date().getFullYear() - new Date(p.dob).getFullYear()}</td>
      <td>${p.doctor}</td>
      <td>${statusBadge(p.status)}</td>
    </tr>
  `).join('');
}

function renderUpcomingAppointments() {
  const container = document.getElementById('upcoming-appointments');
  const todayStr = new Date().toISOString().slice(0, 10);
  const today = appointments.filter(a => a.date === todayStr).slice(0, 4);
  container.innerHTML = today.map(a => `
    <div class="appointment-item">
      <div class="appt-time">${a.time}</div>
      <div class="appt-info">
        <div class="appt-patient">${a.patient}</div>
        <div class="appt-doctor">${a.doctor} — ${a.reason}</div>
      </div>
      ${statusBadge(a.status)}
    </div>
  `).join('');
}

function renderPatients(list) {
  const tbody = document.getElementById('patients-table');
  tbody.innerHTML = list.map(p => `
    <tr>
      <td><code style="font-size:12px;color:var(--text-muted)">${p.id}</code></td>
      <td><strong>${p.name}</strong></td>
      <td>${formatDate(p.dob)}</td>
      <td>${p.phone}</td>
      <td>${p.doctor}</td>
      <td>${statusBadge(p.status)}</td>
      <td>
        <div class="action-btns">
          <button class="btn btn-sm btn-outline" onclick="viewPatient('${p.id}')">Voir</button>
          <button class="btn btn-sm btn-primary" onclick="editPatient('${p.id}')">Modifier</button>
        </div>
      </td>
    </tr>
  `).join('');
}

function renderAppointments(list) {
  const tbody = document.getElementById('appointments-table');
  tbody.innerHTML = list.map(a => `
    <tr>
      <td><strong>${a.patient}</strong></td>
      <td>${a.doctor}</td>
      <td>${formatDate(a.date)}</td>
      <td>${a.time}</td>
      <td>${a.reason}</td>
      <td>${statusBadge(a.status)}</td>
    </tr>
  `).join('');
}

function renderDoctors() {
  const grid = document.getElementById('doctors-grid');
  grid.innerHTML = doctors.map(d => `
    <div class="doctor-card">
      <div class="doctor-avatar">${initials(d.name)}</div>
      <div class="doctor-name">${d.name}</div>
      <div class="doctor-specialty">${d.specialty}</div>
      <span class="badge ${d.available ? 'badge-success' : 'badge-danger'}" style="margin-bottom:14px">
        ${d.available ? 'Disponible' : 'Indisponible'}
      </span>
      <div class="doctor-stats">
        <span><strong>${d.patients}</strong>Patients</span>
        <span><strong>${d.experience}</strong>Expérience</span>
      </div>
    </div>
  `).join('');
}

function renderCharts() {
  const maxCount = Math.max(...admissions.map(a => a.count));
  const barsEl = document.getElementById('chart-admissions');
  barsEl.innerHTML = admissions.map(a => `
    <div class="bar-wrap">
      <div class="bar" style="height:${Math.round((a.count / maxCount) * 100)}%"
           title="${a.count} admissions"></div>
      <div class="bar-label">${a.month}</div>
    </div>
  `).join('');

  const pieEl = document.getElementById('pie-specialties');
  pieEl.innerHTML = specialties.map(s => `
    <div class="legend-item">
      <div class="legend-dot" style="background:${s.color}"></div>
      <span style="min-width:120px;font-size:13px">${s.label}</span>
      <div class="legend-bar-bg">
        <div class="legend-bar-fill" style="width:${s.pct}%;background:${s.color}"></div>
      </div>
      <span class="legend-pct">${s.pct}%</span>
    </div>
  `).join('');
}

/* ===== Navigation ===== */
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const pageTitle = document.getElementById('page-title');

const titles = {
  dashboard: 'Tableau de bord',
  patients: 'Patients',
  appointments: 'Rendez-vous',
  doctors: 'Médecins',
  reports: 'Rapports',
};

navLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = link.dataset.section;
    navLinks.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    sections.forEach(s => s.classList.remove('active'));
    document.getElementById(`section-${target}`).classList.add('active');
    pageTitle.textContent = titles[target] || target;
  });
});

/* ===== Search ===== */
document.getElementById('patient-search').addEventListener('input', function () {
  const q = this.value.toLowerCase();
  renderPatients(patients.filter(p =>
    p.name.toLowerCase().includes(q) ||
    p.doctor.toLowerCase().includes(q) ||
    p.id.toLowerCase().includes(q)
  ));
});

document.getElementById('appointment-search').addEventListener('input', function () {
  const q = this.value.toLowerCase();
  renderAppointments(appointments.filter(a =>
    a.patient.toLowerCase().includes(q) ||
    a.doctor.toLowerCase().includes(q) ||
    a.reason.toLowerCase().includes(q)
  ));
});

/* ===== Modal ===== */
const overlay = document.getElementById('modal-overlay');
const modalTitle = document.getElementById('modal-title');
const modalBody = document.getElementById('modal-body');

function openModal(title, bodyHTML) {
  modalTitle.textContent = title;
  modalBody.innerHTML = bodyHTML;
  overlay.classList.add('open');
}

function closeModal() {
  overlay.classList.remove('open');
}

document.getElementById('modal-close').addEventListener('click', closeModal);
overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });

/* ===== Add button ===== */
const addBtn = document.getElementById('add-btn');
const activeSection = () => document.querySelector('.nav-link.active').dataset.section;

addBtn.addEventListener('click', () => {
  const section = activeSection();
  if (section === 'patients') {
    openModal('Ajouter un patient', patientForm());
  } else if (section === 'appointments') {
    openModal('Nouveau rendez-vous', appointmentForm());
  } else if (section === 'doctors') {
    openModal('Ajouter un médecin', doctorForm());
  } else {
    openModal('Information', '<p style="color:var(--text-muted);text-align:center;padding:20px 0">Sélectionnez une section pour ajouter un élément.</p>');
  }
});

function patientForm() {
  return `
    <form onsubmit="submitPatientForm(event)">
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Prénom</label>
          <input class="form-input" name="firstname" required placeholder="Prénom" />
        </div>
        <div class="form-group">
          <label class="form-label">Nom</label>
          <input class="form-input" name="lastname" required placeholder="Nom" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Date de naissance</label>
          <input class="form-input" name="dob" type="date" required />
        </div>
        <div class="form-group">
          <label class="form-label">Téléphone</label>
          <input class="form-input" name="phone" placeholder="+221 XX XXX XXXX" />
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Médecin traitant</label>
        <select class="form-select" name="doctor">
          ${doctors.map(d => `<option>${d.name}</option>`).join('')}
        </select>
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-outline" onclick="closeModal()">Annuler</button>
        <button type="submit" class="btn btn-primary">Enregistrer</button>
      </div>
    </form>`;
}

function appointmentForm() {
  return `
    <form onsubmit="submitAppointmentForm(event)">
      <div class="form-group">
        <label class="form-label">Patient</label>
        <select class="form-select" name="patient">
          ${patients.map(p => `<option>${p.name}</option>`).join('')}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Médecin</label>
        <select class="form-select" name="doctor">
          ${doctors.map(d => `<option>${d.name}</option>`).join('')}
        </select>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Date</label>
          <input class="form-input" name="date" type="date" required />
        </div>
        <div class="form-group">
          <label class="form-label">Heure</label>
          <input class="form-input" name="time" type="time" required />
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Motif</label>
        <input class="form-input" name="reason" placeholder="Motif de la consultation" required />
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-outline" onclick="closeModal()">Annuler</button>
        <button type="submit" class="btn btn-primary">Confirmer</button>
      </div>
    </form>`;
}

function doctorForm() {
  return `
    <form onsubmit="submitDoctorForm(event)">
      <div class="form-group">
        <label class="form-label">Nom complet</label>
        <input class="form-input" name="name" required placeholder="Dr. Nom Prénom" />
      </div>
      <div class="form-group">
        <label class="form-label">Spécialité</label>
        <select class="form-select" name="specialty">
          <option>Médecine générale</option>
          <option>Cardiologie</option>
          <option>Pédiatrie</option>
          <option>Radiologie</option>
          <option>Chirurgie</option>
          <option>Gynécologie</option>
          <option>Neurologie</option>
          <option>Dermatologie</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Années d'expérience</label>
        <input class="form-input" name="experience" type="number" min="0" placeholder="5" />
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-outline" onclick="closeModal()">Annuler</button>
        <button type="submit" class="btn btn-primary">Ajouter</button>
      </div>
    </form>`;
}

/* ===== Form submissions ===== */
function submitPatientForm(e) {
  e.preventDefault();
  const fd = new FormData(e.target);
  const newPatient = {
    id: `P${String(patients.length + 1).padStart(3, '0')}`,
    name: `${fd.get('firstname')} ${fd.get('lastname')}`,
    dob: fd.get('dob'),
    phone: fd.get('phone') || '—',
    doctor: fd.get('doctor'),
    status: 'Actif',
  };
  patients.unshift(newPatient);
  document.getElementById('stat-patients').textContent = patients.length;
  renderPatients(patients);
  renderRecentPatients();
  closeModal();
}

function submitAppointmentForm(e) {
  e.preventDefault();
  const fd = new FormData(e.target);
  const newAppt = {
    patient: fd.get('patient'),
    doctor: fd.get('doctor'),
    date: fd.get('date'),
    time: fd.get('time'),
    reason: fd.get('reason'),
    status: 'En attente',
  };
  appointments.unshift(newAppt);
  document.getElementById('stat-appointments').textContent = appointments.length;
  renderAppointments(appointments);
  closeModal();
}

function submitDoctorForm(e) {
  e.preventDefault();
  const fd = new FormData(e.target);
  const newDoc = {
    name: fd.get('name'),
    specialty: fd.get('specialty'),
    patients: 0,
    experience: `${fd.get('experience')} ans`,
    available: true,
  };
  doctors.push(newDoc);
  document.getElementById('stat-doctors').textContent = doctors.length;
  renderDoctors();
  closeModal();
}

/* ===== Patient actions ===== */
function viewPatient(id) {
  const p = patients.find(x => x.id === id);
  if (!p) return;
  openModal(`Dossier patient — ${p.id}`, `
    <div style="display:grid;gap:12px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div><div style="font-size:12px;color:var(--text-muted);font-weight:600;margin-bottom:4px">NOM COMPLET</div><div style="font-weight:600">${p.name}</div></div>
        <div><div style="font-size:12px;color:var(--text-muted);font-weight:600;margin-bottom:4px">DATE DE NAISSANCE</div><div>${formatDate(p.dob)}</div></div>
        <div><div style="font-size:12px;color:var(--text-muted);font-weight:600;margin-bottom:4px">TÉLÉPHONE</div><div>${p.phone}</div></div>
        <div><div style="font-size:12px;color:var(--text-muted);font-weight:600;margin-bottom:4px">MÉDECIN TRAITANT</div><div>${p.doctor}</div></div>
        <div><div style="font-size:12px;color:var(--text-muted);font-weight:600;margin-bottom:4px">STATUT</div><div>${statusBadge(p.status)}</div></div>
        <div><div style="font-size:12px;color:var(--text-muted);font-weight:600;margin-bottom:4px">ID</div><div style="font-family:monospace">${p.id}</div></div>
      </div>
      <div class="form-actions" style="margin-top:8px">
        <button class="btn btn-outline" onclick="closeModal()">Fermer</button>
      </div>
    </div>
  `);
}

function editPatient(id) {
  const p = patients.find(x => x.id === id);
  if (!p) return;
  const [first, ...rest] = p.name.split(' ');
  openModal(`Modifier — ${p.name}`, `
    <form onsubmit="saveEditPatient(event,'${id}')">
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Prénom</label>
          <input class="form-input" name="firstname" value="${first}" required />
        </div>
        <div class="form-group">
          <label class="form-label">Nom</label>
          <input class="form-input" name="lastname" value="${rest.join(' ')}" required />
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Téléphone</label>
        <input class="form-input" name="phone" value="${p.phone}" />
      </div>
      <div class="form-group">
        <label class="form-label">Statut</label>
        <select class="form-select" name="status">
          <option ${p.status === 'Actif' ? 'selected' : ''}>Actif</option>
          <option ${p.status === 'En traitement' ? 'selected' : ''}>En traitement</option>
          <option ${p.status === 'Sorti' ? 'selected' : ''}>Sorti</option>
        </select>
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-outline" onclick="closeModal()">Annuler</button>
        <button type="submit" class="btn btn-primary">Sauvegarder</button>
      </div>
    </form>
  `);
}

function saveEditPatient(e, id) {
  e.preventDefault();
  const fd = new FormData(e.target);
  const p = patients.find(x => x.id === id);
  if (!p) return;
  p.name = `${fd.get('firstname')} ${fd.get('lastname')}`;
  p.phone = fd.get('phone');
  p.status = fd.get('status');
  renderPatients(patients);
  renderRecentPatients();
  closeModal();
}

/* ===== Date display ===== */
function updateDate() {
  const now = new Date();
  document.getElementById('current-date').textContent = now.toLocaleDateString('fr-FR', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
}

/* ===== Init ===== */
(function init() {
  updateDate();
  renderRecentPatients();
  renderUpcomingAppointments();
  renderPatients(patients);
  renderAppointments(appointments);
  renderDoctors();
  renderCharts();
})();
