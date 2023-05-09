&lt;svg fill=&quot;none&quot; viewBox=&quot;0 0 600 300&quot; width=&quot;600&quot; height=&quot;300&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;&gt;
  &lt;foreignObject width=&quot;100%&quot; height=&quot;100%&quot;&gt;
    &lt;div xmlns=&quot;http://www.w3.org/1999/xhtml&quot;&gt;
      &lt;style&gt;
        @keyframes hi  {
            0% { transform: rotate( 0.0deg) }
           10% { transform: rotate(14.0deg) }
           20% { transform: rotate(-8.0deg) }
           30% { transform: rotate(14.0deg) }
           40% { transform: rotate(-4.0deg) }
           50% { transform: rotate(10.0deg) }
           60% { transform: rotate( 0.0deg) }
          100% { transform: rotate( 0.0deg) }
        }

        @keyframes gradient {
          0% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
          100% {
            background-position: 0% 50%;
          }
        }

        .container {
          --color-main: #1f4576;
          --color-primary: #3e92cc;
          --color-secondary: #5bc0be;
          --color-tertiary: #e6f2ff;

          background: linear-gradient(-45deg, var(--color-main), var(--color-primary), var(--color-secondary), var(--color-tertiary));
          background-size: 400% 400%;
          animation: gradient 15s ease infinite;

          width: 100%;
          height: 300px;

          display: flex;
          justify-content: center;
          align-items: center;
          color: white;

          font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Helvetica, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;;
        }

        .hi {
          animation: hi 1.5s linear -0.5s infinite;
          display: inline-block;
          transform-origin: 70% 70%;
        }

        @media (prefers-reduced-motion) {
          .container {
            animation: none;
          }

          .hi {
            animation: none;
          }
        }
      &lt;/style&gt;

      &lt;div class=&quot;container&quot;&gt;
        &lt;h1&gt;Hi there, Diego here &lt;div class=&quot;hi&quot;&gt;&amp;#x1F44B;&lt;/div&gt;&lt;/h1&gt;
        &lt;p&gt;Check out my portfolio at &lt;a href=&quot;https://www.datascienceportfol.io/diegosvbrito&quot; style=&quot;color: white;&quot;&gt;www.datascienceportfol.io/diegosvbrito&lt;/a&gt;&lt;/p&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/foreignObject&gt;
&lt;/svg&gt;
