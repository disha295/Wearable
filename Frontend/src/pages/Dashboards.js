import React, { useEffect } from "react";

const Dashboards = () => {
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://public.tableau.com/javascripts/api/viz_v1.js";
    script.async = true;
    document.getElementById("vizCardio")?.appendChild(script.cloneNode());
    document.getElementById("vizSleep")?.appendChild(script.cloneNode());
    document.getElementById("vizAnomaly")?.appendChild(script.cloneNode());
  }, []);

  const dashboards = [
    {
      id: "vizCardio",
      title: "❤️ Cardiovascular Health",
      description:
        "Visualizes metrics like VO₂ Max, HRV, RHR, and HR Recovery to monitor aerobic fitness, autonomic balance, and recovery patterns. Z-score thresholds flag anomalies, enabling early detection of physiological disruptions.",
      img: "https://public.tableau.com/static/images/Ca/Cardinovascularhealthdashboard/Dashboard1/1_rss.png",
      name: "Cardinovascularhealthdashboard/Dashboard1",
      textColor: "text-red-700",
    },
    {
      id: "vizSleep",
      title: "🛌 Sleep, Activity & Lifestyle",
      description:
        "Combines sleep consistency, noise exposure, daylight, and activity patterns to provide a holistic overview of wellness. Color-coded insights indicate when environmental and behavioral stressors align.",
      img: "https://public.tableau.com/static/images/Sl/SleepActivityandLifestyleDashboard/Dashboard1/1_rss.png",
      name: "SleepActivityandLifestyleDashboard/Dashboard1",
      textColor: "text-indigo-700",
    },
    {
      id: "vizAnomaly",
      title: "📈 Multi-Metric Anomaly Detection",
      description:
        "Detects outliers across diverse metrics like body weight, hydration, HR, and oxygen saturation. Highlights abrupt changes or chronic issues using statistical z-score thresholds and contextual annotations.",
      img: "https://public.tableau.com/static/images/Mu/Multi-metricanomalydetectionsystem/Dashboard1/1_rss.png",
      name: "Multi-metricanomalydetectionsystem/Dashboard1",
      textColor: "text-orange-700",
    },
  ];

  return (
    <div className="bg-gray-50 min-h-screen py-10 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
          📊 <span className="ml-2">Tableau Dashboards</span>
        </h1>
        <p className="text-gray-600 mb-10 text-sm">
          Visualize health trends and detect anomalies across multiple domains.
        </p>

        {dashboards.map(({ id, title, description, img, name, textColor }) => (
          <section key={id} className="mb-12">
            <h2 className={`text-2xl font-semibold mb-1 ${textColor}`}>
              {title}
            </h2>
            <p className="text-gray-700 mb-4">{description}</p>
            <div
              className="tableauPlaceholder overflow-hidden rounded-xl border shadow bg-white"
              id={id}
              style={{ height: "900px", position: "relative" }}
            >
              <noscript>
                <a href="#">
                  <img alt={title} src={img} style={{ border: "none" }} />
                </a>
              </noscript>
              <object className="tableauViz w-full h-full">
                <param
                  name="host_url"
                  value="https%3A%2F%2Fpublic.tableau.com%2F"
                />
                <param name="embed_code_version" value="3" />
                <param name="site_root" value="" />
                <param name="name" value={name} />
                <param name="tabs" value="no" />
                <param name="toolbar" value="yes" />
                <param name="animate_transition" value="yes" />
                <param name="display_static_image" value="yes" />
                <param name="display_spinner" value="yes" />
                <param name="display_overlay" value="yes" />
                <param name="display_count" value="yes" />
                <param name="language" value="en-US" />
                <param name="filter" value="publish=yes" />
              </object>
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};

export default Dashboards;
