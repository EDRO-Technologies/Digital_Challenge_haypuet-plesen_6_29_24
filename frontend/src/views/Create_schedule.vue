<!-- <!-- <script setup>
import { ref } from "vue";

</script>

<template>
  <main>
    <div class="mb-3">
  <label for="formFile" class="form-label">Выгрузка данных из Excel файла</label>
  <input class="form-control" type="file" id="formFile">
</div>

  </main>
</template> -->
<!-- 
<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">📚 UniSchedule</a>
        <button class="navbar-toggler" type="button" @click="toggleNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ show: navOpen }">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" :class="{ active: currentView === 'schedule' }" 
                 @click="currentView = 'schedule'" href="#">
                Расписание
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" :class="{ active: currentView === 'add' }" 
                 @click="currentView = 'add'" href="#">
                Добавить
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid px-4">

      <div v-if="currentView === 'schedule'" class="schedule-view">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h1 class="display-5 fw-bold text-dark">Расписание занятий</h1>
          <select v-model="selectedGroup" class="form-select form-select-lg" style="width: auto;">
            <option value="">Все группы</option>
            <option v-for="group in uniqueGroups" :key="group" :value="group">
              {{ group }}
            </option>
          </select>
        </div>

        <div v-if="filteredSchedules.length === 0" class="alert alert-info">
          <h4 class="alert-heading">📋 Расписание пусто</h4>
          <p class="mb-0">Начните с добавления занятий.</p>
        </div>

        <div class="row">
          <div v-for="day in weekDays" :key="day" class="col-12 col-md-6 col-xl-4 mb-4">
            <div class="card shadow-sm h-100 border-0">
              <div class="card-header bg-dark text-white">
                <h5 class="mb-0 fw-semibold">{{ day }}</h5>
              </div>
              <div class="card-body p-0">
                <div v-if="getSchedulesByDay(day).length === 0" class="p-4 text-center text-muted">
                  <small>Нет занятий</small>
                </div>
                <div v-else class="list-group list-group-flush">
                  <div v-for="schedule in getSchedulesByDay(day)" :key="schedule.id"
                       class="list-group-item list-group-item-action py-3">
                    <div class="d-flex justify-content-between align-items-start">
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center gap-2 mb-2">
                          <span class="badge bg-dark">{{ schedule.time }}</span>
                          <span class="badge bg-secondary">{{ schedule.group }}</span>
                        </div>
                        <h6 class="mb-1 fw-semibold">{{ schedule.subject }}</h6>
                        <p class="mb-1 small text-muted">
                          👨‍🏫 {{ schedule.teacher }}
                        </p>
                        <p class="mb-0 small text-muted">
                          🏫 {{ schedule.room }}
                        </p>
                      </div>
                      <div class="d-flex flex-column gap-1">
                        <button @click="editSchedule(schedule)" 
                                class="btn btn-sm btn-outline-primary">
                          ✏️
                        </button>
                        <button @click="deleteSchedule(schedule.id)" 
                                class="btn btn-sm btn-outline-danger">
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="form-view">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-8 col-xl-6">
            <div class="card shadow border-0">
              <div class="card-header bg-dark text-white">
                <h2 class="mb-0 fw-semibold">
                  {{ editingSchedule ? '✏️ Редактировать' : '➕ Добавить' }} занятие
                </h2>
              </div>
              <div class="card-body p-4">
                <form @submit.prevent="handleSubmit">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Предмет</label>
                      <input v-model="form.subject" type="text" 
                             class="form-control form-control-lg"
                             placeholder="Например: Математика" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Преподаватель</label>
                      <input v-model="form.teacher" type="text" 
                             class="form-control form-control-lg"
                             placeholder="ФИО преподавателя" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Группа</label>
                      <input v-model="form.group" type="text" 
                             class="form-control form-control-lg"
                             placeholder="Например: ИС-21-1" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Аудитория</label>
                      <input v-model="form.room" type="text" 
                             class="form-control form-control-lg"
                             placeholder="Например: 305" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">День недели</label>
                      <select v-model="form.day" class="form-select form-select-lg" required>
                        <option value="">Выберите день</option>
                        <option v-for="day in weekDays" :key="day" :value="day">
                          {{ day }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Время</label>
                      <input v-model="form.time" type="time" 
                             class="form-control form-control-lg" required>
                    </div>
                    <div class="col-12">
                      <div class="d-flex gap-2 justify-content-end mt-3">
                        <button type="button" @click="cancelForm" 
                                class="btn btn-lg btn-secondary">
                          Отмена
                        </button>
                        <button type="submit" class="btn btn-lg btn-dark">
                          {{ editingSchedule ? 'Сохранить' : 'Добавить' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const currentView = ref('schedule')
const navOpen = ref(false)
const selectedGroup = ref('')
const editingSchedule = ref(null)

const weekDays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

const schedules = ref([
  {
    id: 1,
    subject: 'Математический анализ',
    teacher: 'Иванов И.И.',
    group: 'ИС-21-1',
    room: '305',
    day: 'Понедельник',
    time: '09:00'
  },
  {
    id: 2,
    subject: 'Программирование',
    teacher: 'Петров П.П.',
    group: 'ИС-21-1',
    room: '412',
    day: 'Понедельник',
    time: '10:45'
  },
  {
    id: 3,
    subject: 'Базы данных',
    teacher: 'Сидоров С.С.',
    group: 'ИС-21-2',
    room: '208',
    day: 'Вторник',
    time: '09:00'
  }
])

const nextId = ref(4)

const form = reactive({
  subject: '',
  teacher: '',
  group: '',
  room: '',
  day: '',
  time: ''
})

const filteredSchedules = computed(() => {
  if (!selectedGroup.value) return schedules.value
  return schedules.value.filter(s => s.group === selectedGroup.value)
})

const uniqueGroups = computed(() => {
  const groups = new Set(schedules.value.map(s => s.group))
  return Array.from(groups).sort()
})

const getSchedulesByDay = (day) => {
  return filteredSchedules.value
    .filter(s => s.day === day)
    .sort((a, b) => a.time.localeCompare(b.time))
}

const toggleNav = () => {
  navOpen.value = !navOpen.value
}

const editSchedule = (schedule) => {
  editingSchedule.value = schedule
  form.subject = schedule.subject
  form.teacher = schedule.teacher
  form.group = schedule.group
  form.room = schedule.room
  form.day = schedule.day
  form.time = schedule.time
  currentView.value = 'add'
}

const deleteSchedule = (id) => {
  if (confirm('Вы уверены, что хотите удалить это занятие?')) {
    schedules.value = schedules.value.filter(s => s.id !== id)
  }
}

const handleSubmit = () => {
  if (editingSchedule.value) {
    const index = schedules.value.findIndex(s => s.id === editingSchedule.value.id)
    schedules.value[index] = {
      ...editingSchedule.value,
      ...form
    }
  } else {
    schedules.value.push({
      id: nextId.value++,
      ...form
    })
  }
  cancelForm()
}

const cancelForm = () => {
  editingSchedule.value = null
  form.subject = ''
  form.teacher = ''
  form.group = ''
  form.room = ''
  form.day = ''
  form.time = ''
  currentView.value = 'schedule'
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar-dark {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
}

.navbar-brand {
  font-size: 1.5rem;
  cursor: pointer;
}

.nav-link {
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
  border-radius: 4px;
  margin: 0 0.25rem;
  cursor: pointer;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 500;
}

.card {
  transition: transform 0.2s ease;
  border-radius: 8px;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-2px);
}

.card-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-bottom: 3px solid #007bff;
  padding: 1rem;
}

.list-group-item {
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
}

.list-group-item:hover {
  border-left-color: #007bff;
  background-color: #f8f9fa;
}

.form-control, .form-select {
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #1a1a1a;
  box-shadow: 0 0 0 0.2rem rgba(26, 26, 26, 0.1);
}

.btn-dark {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border: none;
}

.btn-dark:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>  -->


<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">📚 UniSchedule</a>
        <button class="navbar-toggler" type="button" @click="toggleNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ show: navOpen }">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" :class="{ active: currentView === 'calendar' }" 
                 @click="currentView = 'calendar'" href="#">
                Календарь
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" :class="{ active: currentView === 'schedule' }" 
                 @click="currentView = 'schedule'" href="#">
                Расписание
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" :class="{ active: currentView === 'add' }" 
                 @click="currentView = 'add'" href="#">
                Добавить
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid px-4">
      <!-- Календарь занятий -->
      <div v-if="currentView === 'calendar'" class="calendar-view">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h1 class="display-5 fw-bold text-dark">Календарь занятий</h1>
          <select v-model="selectedGroup" class="form-select form-select-lg" style="width: auto;">
            <option value="">Все группы</option>
            <option v-for="group in uniqueGroups" :key="group" :value="group">
              {{ group }}
            </option>
          </select>
        </div>
        
        <div class="card shadow border-0">
          <div class="card-body p-4">
            <FullCalendar :options="calendarOptions" />
          </div>
        </div>
      </div>

      <!-- Просмотр расписания -->
      <div v-else-if="currentView === 'schedule'" class="schedule-view">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h1 class="display-5 fw-bold text-dark">Расписание занятий</h1>
          <select v-model="selectedGroup" class="form-select form-select-lg" style="width: auto;">
            <option value="">Все группы</option>
            <option v-for="group in uniqueGroups" :key="group" :value="group">
              {{ group }}
            </option>
          </select>
        </div>

        <div v-if="filteredSchedules.length === 0" class="alert alert-info">
          <h4 class="alert-heading">📋 Расписание пусто</h4>
          <p class="mb-0">Начните с добавления занятий.</p>
        </div>

        <div class="row">
          <div v-for="day in weekDays" :key="day" class="col-12 col-md-6 col-xl-4 mb-4">
            <div class="card shadow-sm h-100 border-0">
              <div class="card-header bg-dark text-white">
                <h5 class="mb-0 fw-semibold">{{ day }}</h5>
              </div>
              <div class="card-body p-0">
                <div v-if="getSchedulesByDay(day).length === 0" class="p-4 text-center text-muted">
                  <small>Нет занятий</small>
                </div>
                <div v-else class="list-group list-group-flush">
                  <div v-for="schedule in getSchedulesByDay(day)" :key="schedule.id"
                       class="list-group-item list-group-item-action py-3">
                    <div class="d-flex justify-content-between align-items-start">
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center gap-2 mb-2">
                          <span class="badge bg-dark">{{ schedule.time }}</span>
                          <span class="badge bg-secondary">{{ schedule.group }}</span>
                        </div>
                        <h6 class="mb-1 fw-semibold">{{ schedule.subject }}</h6>
                        <p class="mb-1 small text-muted">
                          👨‍🏫 {{ schedule.teacher }}
                        </p>
                        <p class="mb-0 small text-muted">
                          🏫 {{ schedule.room }}
                        </p>
                      </div>
                      <div class="d-flex flex-column gap-1">
                        <button @click="editSchedule(schedule)" 
                                class="btn btn-sm btn-outline-primary">
                          ✏️
                        </button>
                        <button @click="deleteSchedule(schedule.id)" 
                                class="btn btn-sm btn-outline-danger">
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Форма добавления/редактирования -->
      <div v-else class="form-view">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-8 col-xl-6">
            <div class="card shadow border-0">
              <div class="card-header bg-dark text-white">
                <h2 class="mb-0 fw-semibold">
                  {{ editingSchedule ? '✏️ Редактировать' : '➕ Добавить' }} занятие
                </h2>
              </div>
              <div class="card-body p-4">
                <form @submit.prevent="handleSubmit">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Предмет</label>
                      <input v-model="form.subject" type="text" 
                             class="form-control form-control-lg"
                             placeholder="Например: Математика" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Преподаватель</label>
                      <input v-model="form.teacher" type="text" 
                             class="form-control form-control-lg"
                             placeholder="ФИО преподавателя" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Группа</label>
                      <input v-model="form.group" type="text" 
                             class="form-control form-control-lg"
                             placeholder="Например: ИС-21-1" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Аудитория</label>
                      <input v-model="form.room" type="text" 
                             class="form-control form-control-lg"
                             placeholder="Например: 305" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">День недели</label>
                      <select v-model="form.day" class="form-select form-select-lg" required>
                        <option value="">Выберите день</option>
                        <option v-for="day in weekDays" :key="day" :value="day">
                          {{ day }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-semibold">Время</label>
                      <input v-model="form.time" type="time" 
                             class="form-control form-control-lg" required>
                    </div>
                    <div class="col-12">
                      <div class="d-flex gap-2 justify-content-end mt-3">
                        <button type="button" @click="cancelForm" 
                                class="btn btn-lg btn-secondary">
                          Отмена
                        </button>
                        <button type="submit" class="btn btn-lg btn-dark">
                          {{ editingSchedule ? 'Сохранить' : 'Добавить' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import ruLocale from '@fullcalendar/core/locales/ru'

const currentView = ref('schedule')
const navOpen = ref(false)
const selectedGroup = ref('')
const editingSchedule = ref(null)

const weekDays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

const schedules = ref([
  {
    id: 1,
    subject: 'Математический анализ',
    teacher: 'Иванов И.И.',
    group: 'ИС-21-1',
    room: '305',
    day: 'Понедельник',
    time: '09:00'
  },
  {
    id: 2,
    subject: 'Программирование',
    teacher: 'Петров П.П.',
    group: 'ИС-21-1',
    room: '412',
    day: 'Понедельник',
    time: '10:45'
  },
  {
    id: 3,
    subject: 'Базы данных',
    teacher: 'Сидоров С.С.',
    group: 'ИС-21-2',
    room: '208',
    day: 'Вторник',
    time: '09:00'
  }
])

const nextId = ref(4)

const form = reactive({
  subject: '',
  teacher: '',
  group: '',
  room: '',
  day: '',
  time: ''
})

const filteredSchedules = computed(() => {
  if (!selectedGroup.value) return schedules.value
  return schedules.value.filter(s => s.group === selectedGroup.value)
})

const uniqueGroups = computed(() => {
  const groups = new Set(schedules.value.map(s => s.group))
  return Array.from(groups).sort()
})

const getSchedulesByDay = (day) => {
  return filteredSchedules.value
    .filter(s => s.day === day)
    .sort((a, b) => a.time.localeCompare(b.time))
}

const toggleNav = () => {
  navOpen.value = !navOpen.value
}

const editSchedule = (schedule) => {
  editingSchedule.value = schedule
  form.subject = schedule.subject
  form.teacher = schedule.teacher
  form.group = schedule.group
  form.room = schedule.room
  form.day = schedule.day
  form.time = schedule.time
  currentView.value = 'add'
}

const deleteSchedule = (id) => {
  if (confirm('Вы уверены, что хотите удалить это занятие?')) {
    schedules.value = schedules.value.filter(s => s.id !== id)
  }
}

const handleSubmit = () => {
  if (editingSchedule.value) {
    const index = schedules.value.findIndex(s => s.id === editingSchedule.value.id)
    schedules.value[index] = {
      ...editingSchedule.value,
      ...form
    }
  } else {
    schedules.value.push({
      id: nextId.value++,
      ...form
    })
  }
  cancelForm()
}

const cancelForm = () => {
  editingSchedule.value = null
  form.subject = ''
  form.teacher = ''
  form.group = ''
  form.room = ''
  form.day = ''
  form.time = ''
  currentView.value = 'schedule'
}

const getDayOfWeek = (dayName) => {
  const days = {
    'Понедельник': 1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6
  }
  return days[dayName]
}

const calendarEvents = computed(() => {
  const events = filteredSchedules.value.map(schedule => {
    const dayOfWeek = getDayOfWeek(schedule.day)
    const today = new Date()
    const currentDayOfWeek = today.getDay() === 0 ? 7 : today.getDay()
    const diff = dayOfWeek - currentDayOfWeek
    const targetDate = new Date(today)
    targetDate.setDate(today.getDate() + diff)
    
    const dateStr = targetDate.toISOString().split('T')[0]
    const [hours, minutes] = schedule.time.split(':')
    
    return {
      id: schedule.id,
      title: `${schedule.subject}`,
      start: `${dateStr}T${schedule.time}:00`,
      end: `${dateStr}T${String(parseInt(hours) + 1).padStart(2, '0')}:${minutes}:00`,
      extendedProps: {
        teacher: schedule.teacher,
        room: schedule.room,
        group: schedule.group
      },
      backgroundColor: getGroupColor(schedule.group),
      borderColor: getGroupColor(schedule.group)
    }
  })
  return events
})

const getGroupColor = (group) => {
  const colors = ['#3788d8', '#17a2b8', '#28a745', '#ffc107', '#dc3545', '#6f42c1']
  const hash = group.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[hash % colors.length]
}

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'timeGridWeek',
  locale: ruLocale,
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  events: calendarEvents.value,
  slotMinTime: '08:00:00',
  slotMaxTime: '20:00:00',
  allDaySlot: false,
  height: 'auto',
  eventClick: (info) => {
    const schedule = schedules.value.find(s => s.id === parseInt(info.event.id))
    if (schedule) {
      editSchedule(schedule)
    }
  },
  eventContent: (arg) => {
    return {
      html: `
        <div class="fc-event-main-frame p-1">
          <div class="fw-bold small">${arg.event.title}</div>
          <div class="small">👨‍🏫 ${arg.event.extendedProps.teacher}</div>
          <div class="small">🏫 ${arg.event.extendedProps.room}</div>
          <div class="small">👥 ${arg.event.extendedProps.group}</div>
        </div>
      `
    }
  }
}))
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar-dark {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
}

.navbar-brand {
  font-size: 1.5rem;
  cursor: pointer;
}

.nav-link {
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
  border-radius: 4px;
  margin: 0 0.25rem;
  cursor: pointer;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 500;
}

.card {
  transition: transform 0.2s ease;
  border-radius: 8px;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-2px);
}

.card-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-bottom: 3px solid #007bff;
  padding: 1rem;
}

.list-group-item {
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
}

.list-group-item:hover {
  border-left-color: #007bff;
  background-color: #f8f9fa;
}

.form-control, .form-select {
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #1a1a1a;
  box-shadow: 0 0 0 0.2rem rgba(26, 26, 26, 0.1);
}

.btn-dark {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border: none;
}

.btn-dark:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:deep(.fc) {
  font-family: inherit;
}

:deep(.fc-toolbar-title) {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
}

:deep(.fc-button) {
  background-color: #1a1a1a !important;
  border-color: #1a1a1a !important;
  text-transform: capitalize;
}

:deep(.fc-button:hover) {
  background-color: #2d2d2d !important;
  border-color: #2d2d2d !important;
}

:deep(.fc-button-active) {
  background-color: #007bff !important;
  border-color: #007bff !important;
}

:deep(.fc-event) {
  cursor: pointer;
  border-radius: 4px;
  padding: 2px;
}

:deep(.fc-event:hover) {
  opacity: 0.85;
}

:deep(.fc-daygrid-day-number) {
  font-weight: 600;
  color: #1a1a1a;
}

:deep(.fc-col-header-cell) {
  background-color: #f8f9fa;
  font-weight: 600;
  text-transform: capitalize;
}
</style>
