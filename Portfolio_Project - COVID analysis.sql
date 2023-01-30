select * 
from PortfolioProject.dbo.COVIDDeaths$
order by 3,4

--select * 
--from CovidVaccination
--order by 3,4

-- Select data that will be used
select Location, date, total_cases, new_cases, total_deaths, population_density
from PortfolioProject.dbo.COVIDDeaths$
order by 1,2


-- Total cases vs Total deaths
-- shows likelihodd of dying in your country
select Location, date, total_cases,total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from PortfolioProject.dbo.COVIDDeaths$
where Location like '%Poland%'
order by 1,2


-- Looking at Total Cases vs Population
select Location, date, total_cases, population_density, (total_cases/population_density)*100 as PercentagePopulationInfected
from PortfolioProject.dbo.COVIDDeaths$
where Location like '%Poland%'
order by 1,2

-- Looking at Countries with highest infection rate
select Location,MAX(cast(total_deaths as INT)) as TotalDeathCount
from PortfolioProject.dbo.COVIDDeaths$
-- where Location like '%Poland%'
where continent is not null
group by Location
order by TotalDeathCount desc

-- Break down by continent
-- showing continents with highest death count per population

select continent, MAX(cast(total_deaths as INT)) as TotalDeathCount
from PortfolioProject.dbo.COVIDDeaths$
-- where Location like '%Poland%'
where continent is not null
group by continent
order by TotalDeathCount desc

--GLOBAL NUMBERS

select SUM(new_cases) as total_cases, SUM(cast(new_deaths as INT)) as total_deaths, SUM(cast(new_deaths as INT))/SUM(new_cases)*100 as DeathPercentage
from PortfolioProject.dbo.COVIDDeaths$
-- where Location like '%Poland%'
where continent is not null
-- group by date
order by 1,2


-- total population vs vaccination
Select dea.continent, dea.location, dea.date, vac.population, vac.new_vaccinations
, SUM(convert(int,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location , dea.date) as RollingPeopleVac
-- , (RollingPeopleVac/population)*100 as PercentVaccinated
from PortfolioProject.dbo.COVIDDeaths$ dea
join PortfolioProject..COVIDVaccination vac
 on dea.Location = vac.location
 and dea.date = vac.date
where dea.continent is not null
order by 2,3

-- USE CTE
With PopVSVac (Continent, Location, Date, Popolation, New_Vaccinations, RollingPeopleVac)
as 
(
Select dea.continent, dea.location, dea.date, vac.population, vac.new_vaccinations
, SUM(CONVERT(INT,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location , dea.date) as RollingPeopleVac
-- not posiible to be here
-- (RollingPeopleVac/population)*100 as PercentVaccinated 
from PortfolioProject.dbo.COVIDDeaths$ dea
join PortfolioProject..COVIDVaccination vac
 on dea.Location = vac.location
 and dea.date = vac.date
where dea.continent is not null
-- order by 2,3
)
Select *, (RollingPeopleVac/Popolation)*100 as PercentVaccinated
From PopVSVac


-- TEMP Table
DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVac numeric
)

Insert into #PercentPopulationVaccinated

Select dea.continent, dea.location, dea.date, vac.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location , dea.date) as RollingPeopleVac
-- not posiible to be here
-- (RollingPeopleVac/population)*100 as PercentVaccinated 
from PortfolioProject.dbo.COVIDDeaths$ dea
join PortfolioProject..COVIDVaccination vac
 on dea.Location = vac.location
 and dea.date = vac.date
where dea.continent is not null
-- order by 2,3

Select *
, (RollingPeopleVac/Population)*100 as PercentVaccinated
From #PercentPopulationVaccinated


-- Creating View to store data for later Visualisations
Create View PercentPopulationVaccinated as

Select dea.continent, dea.location, dea.date, vac.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location , dea.date) as RollingPeopleVac
-- not posiible to be here
-- (RollingPeopleVac/population)*100 as PercentVaccinated 
from PortfolioProject.dbo.COVIDDeaths$ dea
join PortfolioProject..COVIDVaccination vac
 on dea.Location = vac.location
 and dea.date = vac.date
where dea.continent is not null
