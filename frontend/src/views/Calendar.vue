<script setup>
import { ref } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import { onMounted } from 'vue'
import axios from 'axios'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

// Конфигурация календаря
const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: "dayGridMonth",
  headerToolbar: {
    left: "prev,next today",
    center: "title",
    right: "dayGridMonth,dayGridWeek,dayGridDay",
  },
    // events:  resp.data,
  // // events: [
    // { title: "Математический анализ", start: new Date(2025, 10, 24, 13, 20) },
    // { title: "Алгебра", start: new Date(2025, 10, 24, 14, 50) },
    // { title: "Алгебра", start: new Date(2025, 10, 24, 16, 20) },
    // { title: "Алгебра", start: new Date(2025, 10, 24, 18, 0) },
  // // ],


  
  editable: true,
  selectable: true,
  locale: "ru",
  dateFormat: {
    hour: "numeric",
    minute: "2-digit",
    omitZeroMinute: true,
    meridiem: "short",
  },
  minute: "2-digit",
  dateClick: handleDateClick,
  eventClick: handleEventClick,
});

// Обработчики событий
function handleDateClick(arg) {
  alert(`Clicked on: ${arg.dateStr}`);
}

function handleEventClick(info) {
  alert(`Event: ${info.event.title}`);
}

const classes = ref([])

const goToSchedule = async (group) => {
    const resp = await axios.get(`http://172.20.10.3:8000/events/by_group_id/${route.params.id}`)

    console.log(resp)

    calendarOptions.value.events = resp.data

    // resp.data 

    // router.push(`/calendar/${resp.data[0].id}`)
    // group.id = resp.data

    // console.log(`Переход к расписанию группы: ${group}`)
    // // window.location.href = `/schedule/${group}` - пример перехода
    // alert(`Переход к расписанию группы: ${group}`)
}

// Lifecycle hook
onMounted(() => {
  // Fetch tasks on page load
  if (route.params.id) goToSchedule()
}
)

</script>

<template>
  <main>
    <FullCalendar :options="calendarOptions" />
  </main>
</template>
