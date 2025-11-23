
    <script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import TheWelcome from '../components/TheWelcome.vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

// Данные программ с группами
const programsData = reactive({
    law: {
        undergraduate: [
            {
                name: "Политология",
                groups: ["ПОЛ-601-51", "ПОЛ-601-52", "ПОЛ-601-41", "ПОЛ-601-42"]
            },
            {
                name: "Юриспруденция", 
                groups: ["ЮР-602-51", "ЮР-602-52", "ЮР-602-41", "ЮР-602-42"]
            }
        ],
        masters: [
            {
                name: "Политология (Государственная политика и управление)",
                groups: ["ПОЛ-701-51", "ПОЛ-701-52"]
            },
            {
                name: "Юриспруденция (Юрист в сфере обеспечения безопасности государства и бизнеса)",
                groups: ["ЮР-702-51", "ЮР-702-52"]
            }
        ]
    },
    humanities: {
        undergraduate: [
            {
                name: "Спорт",
                groups: ["СП-603-51", "СП-603-52", "СП-603-41"]
            },
            {
                name: "История",
                groups: ["ИСТ-604-51", "ИСТ-604-52"]
            },
            {
                name: "Лингвистика",
                groups: ["ЛИН-605-51", "ЛИН-605-52", "ЛИН-605-41"]
            }
        ],
        masters: [
            {
                name: "История (Отечественная история)",
                groups: ["ИСТ-703-51", "ИСТ-703-52"]
            },
            {
                name: "Лингвистика (Лингвистика, лингводидактика и межкультурная коммуникация)",
                groups: ["ЛИН-704-51", "ЛИН-704-52"]
            }
        ]
    },
    science: {
        undergraduate: [
            {
                name: "Биология",
                groups: ["БИО-606-51", "БИО-606-52"]
            },
            {
                name: "Экология и природопользование",
                groups: ["ЭКО-607-51", "ЭКО-607-52"]
            }
        ],
        masters: [
            {
                name: "Биология (Биоразнообразие и охрана природы)",
                groups: ["БИО-705-51"]
            }
        ]
    },
    economics: {
        undergraduate: [
            {
                name: "Экономика",
                groups: ["ЭК-608-51", "ЭК-608-52", "ЭК-608-41"]
            },
            {
                name: "Менеджмент",
                groups: ["МЕН-609-51", "МЕН-609-52"]
            }
        ],
        masters: [
            {
                name: "Экономика (Экономика фирмы и предпринимательство)",
                groups: ["ЭК-706-51", "ЭК-706-52"]
            }
        ]
    },
    medicine: {
        undergraduate: [
            {
                name: "Лечебное дело",
                groups: ["ЛД-610-51", "ЛД-610-52", "ЛД-610-41", "ЛД-610-42"]
            },
            {
                name: "Педиатрия",
                groups: ["ПЕД-611-51", "ПЕД-611-52"]
            }
        ],
        masters: []
    },
    polytech: {
        undergraduate: [
            {
                name: "Информационные системы и технологии",
                groups: ["607-51", "607-52", "607-41", "607-42","607-31", "607-32","607-21", "607-22"]
            },
            {
                name: "Информатика и вычислительная техника", 
                groups: ["606-51", "606-52", "606-41", "606-42","606-31", "606-32","606-21", "606-22"]
            },
            {
                name: "Программная инженерия",
                groups: ["609-51", "609-52", "609-41", "609-42","609-31", "609-32","609-21", "609-22"]
            }
        ],
        masters: [
            {
                name: "Информационные системы и технологии",
                groups: ["607-51", "607-41"]
            },
            {
                name: "Программная инженерия",
                groups: ["609-51", "609-41"]
            }
        ]
    }
})

const instituteNames = {
    law: "Институт государства и права",
    humanities: "Институт гуманитарного образования и спорта", 
    science: "Институт естественных и технических наук",
    economics: "Институт экономики и управления",
    medicine: "Медицинский институт",
    polytech: "Политехнический институт"
}

// Реактивные переменные
const selectedInstitute = ref(null)
const currentStep = ref(1)

// Методы
const selectInstitute = (institute) => {
    selectedInstitute.value = institute
    currentStep.value = 2
}

const goBack = () => {
    selectedInstitute.value = null
    currentStep.value = 1
}



const goToSchedule = async (group) => {
    const resp = await axios.get(`http://172.20.10.3:8000/groups?q=${group}`)

    console.log(resp)

    router.push(`/calendar/${resp.data[0].id}`)
    // group.id = resp.data

    // console.log(`Переход к расписанию группы: ${group}`)
    // // window.location.href = `/schedule/${group}` - пример перехода
    // alert(`Переход к расписанию группы: ${group}`)
}

</script>

<template>
  <main>
    <div class="container my-4">
        <h1 class="text-center mb-4">Образовательные программы</h1>
        
        <!-- Шаг 1: Выбор института -->
        <div v-if="currentStep === 1" id="step1">
            <p class="text-center mb-4">Выберите институт для просмотра образовательных программ</p>
            <div class="row g-3">
                <div class="col-md-6 col-lg-4" v-for="(name, key) in instituteNames" :key="key">
                    <div 
                        class="card institute-card h-100" 
                        :class="{ 'selected': selectedInstitute === key }"
                        @click="selectInstitute(key)"
                    >
                        <div class="card-body">
                            <h5 class="card-title">{{ name }}</h5>
                            <p class="card-text">{{ getInstituteDescription(key) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Шаг 2: Отображение программ -->
        <div v-if="currentStep === 2" id="step2">
            <button class="btn btn-outline-secondary back-btn" @click="goBack">
                ← Назад к выбору института
            </button>
            <div class="card">
                <div class="card-header">
                    <h3 class="institute-name">{{ instituteNames[selectedInstitute] }}</h3>
                </div>
                <div class="card-body">
                    <!-- Бакалавриат/Специалитет -->
                    <div v-if="programsData[selectedInstitute]?.undergraduate?.length" id="undergraduate-section">
                        <h4 class="level-title">Бакалавриат, Специалитет</h4>
                        <div class="programs-list">
                            <div v-for="(program, index) in programsData[selectedInstitute].undergraduate" 
                                 :key="index" class="program-item">
                                <div class="program-header">
                                    <h5 class="program-name">{{ program.name }}</h5>
                                </div>
                                <div class="groups-container">
                                    <div v-for="group in program.groups" :key="group" class="group-item">
                                        <button 
                                            class="btn btn-outline-primary btn-sm group-btn"
                                            @click="goToSchedule(group)"
                                        >
                                            {{ group }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Магистратура -->
                    <div v-if="programsData[selectedInstitute]?.masters?.length" id="masters-section" class="mt-4">
                        <h4 class="level-title">Магистратура</h4>
                        <div class="programs-list">
                            <div v-for="(program, index) in programsData[selectedInstitute].masters" 
                                 :key="index" class="program-item">
                                <div class="program-header">
                                    <h5 class="program-name">{{ program.name }}</h5>
                                </div>
                                <div class="groups-container">
                                    <div v-for="group in program.groups" :key="group" class="group-item">
                                        <button 
                                            class="btn btn-outline-primary btn-sm group-btn"
                                            @click="goToSchedule(group)"
                                        >
                                            {{ group }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Сообщение если нет программ -->
                    <div v-if="!programsData[selectedInstitute]?.undergraduate?.length && 
                               !programsData[selectedInstitute]?.masters?.length" 
                         class="text-center text-muted py-4">
                        Программы не найдены
                    </div>
                </div>
            </div>
        </div>
    </div>
  </main>
</template>

<style scoped>
.institute-card {
    transition: all 0.3s ease;
    cursor: pointer;
    height: 100%;
}
.institute-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.selected {
    border: 2px solid #0d6efd;
    background-color: #f8f9fa;
}
.level-title {
    color: #0d6efd;
    margin-bottom: 1rem;
    border-bottom: 2px solid #0d6efd;
    padding-bottom: 0.5rem;
}
.program-item {
    padding: 1rem 0;
    border-bottom: 1px solid #eee;
}
.program-item:last-child {
    border-bottom: none;
}
.program-header {
    margin-bottom: 0.75rem;
}
.program-name {
    margin: 0;
    color: #495057;
    font-size: 1.1rem;
}
.groups-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
}
.group-item {
    margin-bottom: 0.25rem;
}
.group-btn {
    font-size: 0.85rem;
    padding: 0.25rem 0.75rem;
    transition: all 0.2s ease;
}
.group-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.back-btn {
    margin-bottom: 1rem;
}
.institute-name {
    color: #495057;
    font-weight: bold;
    margin: 0;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
    .groups-container {
        gap: 0.25rem;
    }
    .group-btn {
        font-size: 0.8rem;
        padding: 0.2rem 0.5rem;
    }
    .program-name {
        font-size: 1rem;
    }
}
</style>

<script>
// Вспомогательные функции
export default {
    methods: {
        getInstituteDescription(instituteKey) {
            const descriptions = {
                law: "Программы в области политологии и юриспруденции",
                humanities: "Программы в области спорта, истории, лингвистики, педагогики и психологии", 
                science: "Программы в области биологии, экологии, химии и техносферной безопасности",
                economics: "Программы в области экономики, менеджмента и управления",
                medicine: "Программы в области лечебного дела и педиатрии", 
                polytech: "Программы в области инженерии, информатики и строительства"
            }
            return descriptions[instituteKey] || "Образовательные программы института"
        }
    }
}
</script>