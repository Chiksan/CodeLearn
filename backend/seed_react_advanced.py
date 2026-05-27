"""
Курс "React: продвинутый уровень" — advanced, 8 уроков.
Запуск: docker exec codelearn-backend-1 python seed_react_advanced.py
"""
import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.user import Course, Lesson, LanguageEnum, LevelEnum

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

CDN_HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>body{font-family:Arial,sans-serif;padding:20px;margin:0}button{cursor:pointer}</style>
</head>
<body><div id="root"></div>
<script type="text/babel">"""

CDN_FOOT = "\n</script></body></html>"


def wrap(code): return CDN_HEAD + "\n" + code + CDN_FOOT


LESSONS = [
    {
        "title": "Порталы — модальные окна",
        "order": 1, "xp_reward": 35,
        "content": """## Что такое порталы?

Порталы позволяют рендерить компонент **за пределами** его родительского DOM-узла. Это полезно для модальных окон, тултипов, уведомлений.

```jsx
ReactDOM.createPortal(
  <div className="modal">Контент</div>,
  document.getElementById("modal-root") // куда рендерить
)
```

## Зачем?

Без порталов модальное окно ограничено стилями родителя (overflow: hidden, z-index). Портал позволяет рендерить прямо в `<body>`.

## Пример

```jsx
function Modal({ onClose, children }) {
  return ReactDOM.createPortal(
    <div style={{
      position: 'fixed', top: 0, left: 0,
      width: '100%', height: '100%',
      background: 'rgba(0,0,0,0.5)',
      display: 'flex', alignItems: 'center', justifyContent: 'center'
    }}>
      <div style={{ background: '#fff', padding: '32px', borderRadius: '12px' }}>
        {children}
        <button onClick={onClose}>Закрыть</button>
      </div>
    </div>,
    document.body
  );
}
```

## Задание

Нажми кнопку — откроется модальное окно поверх всего контента. Изучи как работает createPortal.
""",
        "starter_code": wrap("""    function Modal({ onClose, title, children }) {
      return ReactDOM.createPortal(
        <div style={{
          position: 'fixed', inset: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: '#fff', borderRadius: '16px', padding: '32px',
            maxWidth: '400px', width: '90%', boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
          }}>
            <h2 style={{ margin: '0 0 16px' }}>{title}</h2>
            <div style={{ color: '#555', marginBottom: '24px' }}>{children}</div>
            <button onClick={onClose}
              style={{ padding: '10px 24px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '14px' }}>
              Закрыть
            </button>
          </div>
        </div>,
        document.body
      );
    }

    function App() {
      const [open, setOpen] = React.useState(false);

      return (
        <div style={{ padding: '20px' }}>
          <h2>Демо порталов</h2>
          <p>Контент страницы...</p>
          <div style={{ overflow: 'hidden', border: '2px dashed #ddd', padding: '20px', borderRadius: '8px' }}>
            <p>Этот div имеет overflow: hidden — обычное модальное окно было бы обрезано</p>
            <button onClick={() => setOpen(true)}
              style={{ padding: '10px 24px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '8px' }}>
              Открыть модалку
            </button>
          </div>

          {open && (
            <Modal title="Я портал! 🚪" onClose={() => setOpen(false)}>
              <p>Я рендерюсь прямо в document.body, вне любых ограничений родителя.</p>
            </Modal>
          )}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    function Modal({ onClose }) {
      return ReactDOM.createPortal(
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ background: '#fff', padding: '32px', borderRadius: '12px' }}>
            <p>Модальное окно</p>
            <button onClick={onClose}>Закрыть</button>
          </div>
        </div>,
        document.body
      );
    }
    function App() {
      const [open, setOpen] = React.useState(false);
      return <div><button onClick={() => setOpen(true)}>Открыть</button>{open && <Modal onClose={() => setOpen(false)} />}</div>;
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "ReactDOM.createPortal(jsx, domNode) — рендерит jsx в domNode",
            "document.body — стандартное место для модальных окон",
            "position: fixed + inset: 0 растягивает на весь экран"
        ]),
    },
    {
        "title": "Lazy loading и Suspense",
        "order": 2, "xp_reward": 35,
        "content": """## Зачем нужен lazy loading?

При большом приложении весь JS грузится сразу. Это медленно. `React.lazy` позволяет загружать компоненты только когда они нужны.

```jsx
// Обычный импорт (всегда загружается):
import HeavyComponent from './HeavyComponent';

// Ленивый импорт (загружается при первом рендере):
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

## Suspense — граница ожидания

Пока компонент загружается, `Suspense` показывает fallback:

```jsx
<React.Suspense fallback={<div>Загрузка...</div>}>
  <HeavyComponent />
</React.Suspense>
```

## Симуляция без импортов

В CDN-среде мы симулируем lazy через промис:

```jsx
function fakeLazy(factory) {
  return React.lazy(() =>
    new Promise(resolve => setTimeout(() => resolve({ default: factory() }), 1500))
  );
}

const SlowComponent = fakeLazy(() => () => <div>Я загрузился!</div>);
```

## Задание

Нажми кнопку — компонент «загрузится» через 1.5 секунды. Suspense показывает спиннер во время ожидания.
""",
        "starter_code": wrap("""    // Симулируем медленную загрузку компонента
    const HeavyChart = React.lazy(() =>
      new Promise(resolve =>
        setTimeout(() => resolve({
          default: function Chart() {
            return (
              <div style={{ background: '#f0effe', padding: '24px', borderRadius: '12px', marginTop: '16px' }}>
                <h3 style={{ color: '#534AB7' }}>📊 Тяжёлый график</h3>
                <p>Этот компонент загрузился через 1.5 секунды!</p>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end', marginTop: '16px' }}>
                  {[40, 70, 55, 90, 65, 80, 45].map((h, i) => (
                    <div key={i} style={{ width: '32px', height: h + 'px', background: '#534AB7', borderRadius: '4px 4px 0 0' }} />
                  ))}
                </div>
              </div>
            );
          }
        }), 1500)
      )
    );

    function Spinner() {
      return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '24px', color: '#888' }}>
          <div style={{
            width: '24px', height: '24px', border: '3px solid #eee',
            borderTopColor: '#534AB7', borderRadius: '50%',
            animation: 'spin 0.8s linear infinite'
          }} />
          Загружаем компонент...
          <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
        </div>
      );
    }

    function App() {
      const [show, setShow] = React.useState(false);

      return (
        <div style={{ padding: '20px' }}>
          <h2>Lazy Loading демо</h2>
          <button onClick={() => setShow(true)}
            disabled={show}
            style={{ padding: '10px 24px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '14px' }}>
            {show ? 'Загружается...' : 'Загрузить компонент'}
          </button>

          {show && (
            <React.Suspense fallback={<Spinner />}>
              <HeavyChart />
            </React.Suspense>
          )}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    const Lazy = React.lazy(() => new Promise(r => setTimeout(() => r({ default: () => <div>Загружен!</div> }), 1500)));
    function App() {
      const [show, setShow] = React.useState(false);
      return (
        <div>
          <button onClick={() => setShow(true)}>Загрузить</button>
          {show && <React.Suspense fallback={<p>Загрузка...</p>}><Lazy /></React.Suspense>}
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "React.lazy() принимает функцию возвращающую Promise с { default: Component }",
            "Suspense fallback — что показывать пока компонент загружается",
            "Lazy компонент должен быть обёрнут в Suspense"
        ]),
    },
    {
        "title": "Context + Reducer — мини-Redux",
        "order": 3, "xp_reward": 40,
        "content": """## Глобальное состояние без Redux

Комбинация `useContext` + `useReducer` даёт всё что нужно для управления глобальным состоянием.

## Паттерн

```jsx
// 1. Создаём контекст
const StoreContext = React.createContext(null);

// 2. Reducer для логики
function reducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':    return { ...state, items: [...state.items, action.item] };
    case 'REMOVE_ITEM': return { ...state, items: state.items.filter(i => i.id !== action.id) };
    default: return state;
  }
}

// 3. Provider — оборачивает приложение
function StoreProvider({ children }) {
  const [state, dispatch] = React.useReducer(reducer, { items: [] });
  return (
    <StoreContext.Provider value={{ state, dispatch }}>
      {children}
    </StoreContext.Provider>
  );
}

// 4. Хук для удобства
const useStore = () => React.useContext(StoreContext);
```

## Задание

Реализована мини-корзина покупок. Изучи как данные передаются через Context без prop drilling.
""",
        "starter_code": wrap("""    const CartContext = React.createContext(null);

    function cartReducer(state, action) {
      switch (action.type) {
        case 'ADD':
          const exists = state.items.find(i => i.id === action.item.id);
          if (exists) return {
            ...state,
            items: state.items.map(i => i.id === action.item.id ? { ...i, qty: i.qty + 1 } : i)
          };
          return { ...state, items: [...state.items, { ...action.item, qty: 1 }] };
        case 'REMOVE':
          return { ...state, items: state.items.filter(i => i.id !== action.id) };
        case 'CLEAR':
          return { ...state, items: [] };
        default: return state;
      }
    }

    function CartProvider({ children }) {
      const [state, dispatch] = React.useReducer(cartReducer, { items: [] });
      return <CartContext.Provider value={{ state, dispatch }}>{children}</CartContext.Provider>;
    }

    const useCart = () => React.useContext(CartContext);

    const PRODUCTS = [
      { id: 1, name: 'React книга',    price: 2500 },
      { id: 2, name: 'JS курс',        price: 5000 },
      { id: 3, name: 'TypeScript гайд', price: 3000 },
    ];

    function ProductList() {
      const { dispatch } = useCart();
      return (
        <div>
          <h3>🛍 Товары</h3>
          {PRODUCTS.map(p => (
            <div key={p.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', background: '#f8f8fc', borderRadius: '8px', marginBottom: '8px' }}>
              <span>{p.name} — {p.price} тг</span>
              <button onClick={() => dispatch({ type: 'ADD', item: p })}
                style={{ padding: '6px 14px', background: '#534AB7', color: '#fff', border: 'none', borderRadius: '6px' }}>
                + В корзину
              </button>
            </div>
          ))}
        </div>
      );
    }

    function Cart() {
      const { state, dispatch } = useCart();
      const total = state.items.reduce((s, i) => s + i.price * i.qty, 0);
      return (
        <div style={{ marginTop: '20px' }}>
          <h3>🛒 Корзина {state.items.length > 0 && <span style={{ background: '#534AB7', color: '#fff', borderRadius: '50%', padding: '2px 8px', fontSize: '13px' }}>{state.items.length}</span>}</h3>
          {state.items.length === 0
            ? <p style={{ color: '#aaa' }}>Корзина пуста</p>
            : <>
                {state.items.map(i => (
                  <div key={i.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px', borderBottom: '1px solid #eee' }}>
                    <span>{i.name} × {i.qty}</span>
                    <button onClick={() => dispatch({ type: 'REMOVE', id: i.id })} style={{ background: 'none', border: 'none', color: '#e53e3e', cursor: 'pointer' }}>✕</button>
                  </div>
                ))}
                <div style={{ marginTop: '12px', fontWeight: 'bold' }}>Итого: {total} тг</div>
                <button onClick={() => dispatch({ type: 'CLEAR' })} style={{ marginTop: '8px', padding: '6px 14px', background: '#e53e3e', color: '#fff', border: 'none', borderRadius: '6px' }}>Очистить</button>
              </>
          }
        </div>
      );
    }

    function App() {
      return (
        <CartProvider>
          <div style={{ maxWidth: '480px', margin: '0 auto' }}>
            <h2>🏪 Мини-магазин</h2>
            <ProductList />
            <Cart />
          </div>
        </CartProvider>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    const Ctx = React.createContext(null);
    function reducer(state, action) {
      if (action.type === 'ADD') return { items: [...state.items, action.item] };
      if (action.type === 'REMOVE') return { items: state.items.filter(i => i.id !== action.id) };
      return state;
    }
    function Provider({ children }) {
      const [state, dispatch] = React.useReducer(reducer, { items: [] });
      return <Ctx.Provider value={{ state, dispatch }}>{children}</Ctx.Provider>;
    }
    function App() {
      const { state, dispatch } = React.useContext(Ctx);
      return (
        <div>
          <button onClick={() => dispatch({ type: 'ADD', item: { id: Date.now(), name: 'Товар' } })}>Добавить</button>
          {state.items.map(i => <div key={i.id}>{i.name} <button onClick={() => dispatch({ type: 'REMOVE', id: i.id })}>✕</button></div>)}
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<Provider><App /></Provider>);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Provider оборачивает приложение и передаёт { state, dispatch } через Context",
            "useContext(CartContext) читает state и dispatch в любом дочернем компоненте",
            "Reducer обрабатывает все изменения состояния централизованно"
        ]),
    },
    {
        "title": "Compound Components паттерн",
        "order": 4, "xp_reward": 40,
        "content": """## Что такое Compound Components?

Паттерн при котором несколько компонентов работают вместе как одно целое. Классический пример — HTML `<select>` и `<option>`.

```jsx
// Использование:
<Tabs>
  <Tabs.List>
    <Tabs.Tab>Вкладка 1</Tabs.Tab>
    <Tabs.Tab>Вкладка 2</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Контент 1</Tabs.Panel>
  <Tabs.Panel>Контент 2</Tabs.Panel>
</Tabs>
```

## Реализация через Context

```jsx
const TabsContext = React.createContext(null);

function Tabs({ children }) {
  const [active, setActive] = React.useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.Tab = function Tab({ children, index }) {
  const { active, setActive } = React.useContext(TabsContext);
  return (
    <button
      onClick={() => setActive(index)}
      style={{ fontWeight: active === index ? 'bold' : 'normal' }}
    >
      {children}
    </button>
  );
};
```

## Задание

Готовый компонент `Tabs` использует Compound Components паттерн. Изучи как внутренние компоненты общаются через Context.
""",
        "starter_code": wrap("""    const TabsContext = React.createContext(null);

    function Tabs({ children, defaultIndex = 0 }) {
      const [active, setActive] = React.useState(defaultIndex);
      return (
        <TabsContext.Provider value={{ active, setActive }}>
          <div>{children}</div>
        </TabsContext.Provider>
      );
    }

    Tabs.List = function TabList({ children }) {
      return (
        <div style={{ display: 'flex', borderBottom: '2px solid #eee', marginBottom: '16px' }}>
          {React.Children.map(children, (child, i) => React.cloneElement(child, { index: i }))}
        </div>
      );
    };

    Tabs.Tab = function Tab({ children, index }) {
      const { active, setActive } = React.useContext(TabsContext);
      const isActive = active === index;
      return (
        <button
          onClick={() => setActive(index)}
          style={{
            padding: '10px 20px', border: 'none', background: 'none', cursor: 'pointer',
            fontWeight: isActive ? '600' : '400',
            color: isActive ? '#534AB7' : '#666',
            borderBottom: isActive ? '2px solid #534AB7' : '2px solid transparent',
            marginBottom: '-2px', fontSize: '14px'
          }}
        >
          {children}
        </button>
      );
    };

    Tabs.Panel = function Panel({ children, index }) {
      const { active } = React.useContext(TabsContext);
      if (active !== index) return null;
      return <div style={{ padding: '16px', animation: 'fadeIn 0.2s' }}>{children}</div>;
    };

    function App() {
      return (
        <div style={{ maxWidth: '480px', margin: '0 auto', padding: '20px' }}>
          <h2>Compound Components</h2>
          <Tabs>
            <Tabs.List>
              <Tabs.Tab>Python</Tabs.Tab>
              <Tabs.Tab>JavaScript</Tabs.Tab>
              <Tabs.Tab>React</Tabs.Tab>
            </Tabs.List>
            <Tabs.Panel index={0}>
              🐍 Python — отличный язык для начала. Простой синтаксис, огромная экосистема.
            </Tabs.Panel>
            <Tabs.Panel index={1}>
              ⚡ JavaScript — язык веба. Работает в браузере и на сервере (Node.js).
            </Tabs.Panel>
            <Tabs.Panel index={2}>
              ⚛️ React — библиотека для создания интерфейсов. Компонентный подход.
            </Tabs.Panel>
          </Tabs>
          <style>{`@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }`}</style>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    const Ctx = React.createContext(null);
    function Tabs({ children }) {
      const [active, setActive] = React.useState(0);
      return <Ctx.Provider value={{ active, setActive }}><div>{children}</div></Ctx.Provider>;
    }
    Tabs.Tab = function({ children, index }) {
      const { active, setActive } = React.useContext(Ctx);
      return <button onClick={() => setActive(index)} style={{ fontWeight: active===index?'bold':'normal' }}>{children}</button>;
    };
    Tabs.Panel = function({ children, index }) {
      const { active } = React.useContext(Ctx);
      return active === index ? <div>{children}</div> : null;
    };
    function App() {
      return (
        <Tabs>
          <div>{[0,1,2].map(i => <Tabs.Tab key={i} index={i}>Вкладка {i+1}</Tabs.Tab>)}</div>
          {['Контент 1','Контент 2','Контент 3'].map((c,i) => <Tabs.Panel key={i} index={i}>{c}</Tabs.Panel>)}
        </Tabs>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Compound Components общаются через Context — не через props",
            "Tabs.Tab = function() {} — статическое свойство компонента",
            "React.Children.map + cloneElement позволяют передавать index автоматически"
        ]),
    },
    {
        "title": "Виртуализация длинных списков",
        "order": 5, "xp_reward": 35,
        "content": """## Проблема больших списков

Если рендерить 10 000 элементов — браузер будет тормозить. React создаёт DOM-узел для каждого элемента.

## Решение: виртуализация

Рендерим только те элементы, которые видны в viewport. Остальные — не существуют в DOM.

В реальных проектах используют `react-window` или `react-virtual`.

## Самодельная виртуализация

```jsx
function VirtualList({ items, itemHeight, windowHeight }) {
  const [scrollTop, setScrollTop] = React.useState(0);

  const startIdx = Math.floor(scrollTop / itemHeight);
  const visible = Math.ceil(windowHeight / itemHeight) + 1;
  const visibleItems = items.slice(startIdx, startIdx + visible);

  return (
    <div
      style={{ height: windowHeight, overflowY: 'auto' }}
      onScroll={e => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: 'relative' }}>
        {visibleItems.map((item, i) => (
          <div
            key={startIdx + i}
            style={{ position: 'absolute', top: (startIdx + i) * itemHeight, height: itemHeight }}
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Задание

Список из 10 000 элементов рендерится мгновенно благодаря виртуализации. Прокрути — увидишь плавную работу.
""",
        "starter_code": wrap("""    function VirtualList({ items, itemHeight = 48, windowHeight = 400 }) {
      const [scrollTop, setScrollTop] = React.useState(0);

      const startIdx = Math.floor(scrollTop / itemHeight);
      const visibleCount = Math.ceil(windowHeight / itemHeight) + 2;
      const visibleItems = items.slice(startIdx, startIdx + visibleCount);

      return (
        <div
          style={{ height: windowHeight, overflowY: 'auto', border: '1px solid #eee', borderRadius: '8px' }}
          onScroll={e => setScrollTop(e.currentTarget.scrollTop)}
        >
          <div style={{ height: items.length * itemHeight, position: 'relative' }}>
            {visibleItems.map((item, i) => (
              <div
                key={startIdx + i}
                style={{
                  position: 'absolute',
                  top: (startIdx + i) * itemHeight,
                  left: 0, right: 0,
                  height: itemHeight,
                  display: 'flex',
                  alignItems: 'center',
                  padding: '0 16px',
                  borderBottom: '1px solid #f5f5f5',
                  background: (startIdx + i) % 2 === 0 ? '#fff' : '#fafafa'
                }}
              >
                {item}
              </div>
            ))}
          </div>
        </div>
      );
    }

    function App() {
      const items = Array.from({ length: 10000 }, (_, i) =>
        `📌 Элемент #${i + 1} — только видимые рендерятся в DOM`
      );

      return (
        <div style={{ padding: '20px' }}>
          <h2>Виртуализация</h2>
          <p style={{ color: '#888', marginBottom: '16px' }}>
            10 000 элементов — в DOM только ~10 видимых
          </p>
          <VirtualList items={items} />
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    function VList({ items, ih = 48, wh = 300 }) {
      const [scroll, setScroll] = React.useState(0);
      const start = Math.floor(scroll / ih);
      const count = Math.ceil(wh / ih) + 2;
      return (
        <div style={{ height: wh, overflowY: 'auto' }} onScroll={e => setScroll(e.currentTarget.scrollTop)}>
          <div style={{ height: items.length * ih, position: 'relative' }}>
            {items.slice(start, start + count).map((item, i) => (
              <div key={start+i} style={{ position: 'absolute', top: (start+i)*ih, height: ih, display:'flex', alignItems:'center', padding:'0 16px' }}>{item}</div>
            ))}
          </div>
        </div>
      );
    }
    const items = Array.from({length:10000},(_,i)=>`Элемент #${i+1}`);
    ReactDOM.createRoot(document.getElementById('root')).render(<VList items={items} />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Ключевая идея: position: absolute + top = index * itemHeight",
            "Рендерим только slice(startIdx, startIdx + visibleCount)",
            "onScroll отслеживает позицию прокрутки для пересчёта видимых элементов"
        ]),
    },
    {
        "title": "Оптимизация: useMemo и useCallback",
        "order": 6, "xp_reward": 35,
        "content": """## useMemo — кэшируем вычисления

```jsx
const result = React.useMemo(() => {
  return heavyCalculation(data); // пересчитывается только при изменении data
}, [data]);
```

Без `useMemo` — функция вызывается при каждом рендере.

## useCallback — кэшируем функции

```jsx
const handleClick = React.useCallback(() => {
  doSomething(id);
}, [id]); // новая функция только когда id меняется
```

Зачем? При каждом рендере создаётся новая функция. Это ломает `React.memo` дочерних компонентов.

## Когда использовать?

| Хук | Когда |
|-----|-------|
| `useMemo` | Тяжёлые вычисления (сортировка, фильтрация большого массива) |
| `useCallback` | Функции передаются в мемоизированные дочерние компоненты |

**Не оптимизируй всё подряд!** Эти хуки сами имеют стоимость.

## Задание

Большой список фильтруется мгновенно благодаря `useMemo`. Без него браузер тормозил бы при каждом вводе.
""",
        "starter_code": wrap("""    // Симулируем тяжёлые вычисления
    function heavyFilter(items, query) {
      // Имитируем задержку (в реальности был бы сложный алгоритм)
      const start = performance.now();
      while (performance.now() - start < 5) {} // 5ms задержка
      return items.filter(item =>
        item.toLowerCase().includes(query.toLowerCase())
      );
    }

    const ITEMS = Array.from({ length: 2000 }, (_, i) =>
      ['React', 'JavaScript', 'Python', 'TypeScript', 'Node.js', 'Vue', 'Angular'][i % 7] + ` урок ${i + 1}`
    );

    function SearchList() {
      const [query, setQuery] = React.useState('');
      const [count, setCount] = React.useState(0); // для принудительных рендеров

      // useMemo — пересчитываем только при изменении query
      const filtered = React.useMemo(() => {
        return heavyFilter(ITEMS, query);
      }, [query]);

      return (
        <div style={{ padding: '20px' }}>
          <h2>useMemo демо</h2>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Фильтр по названию..."
              style={{ flex: 1, padding: '10px', borderRadius: '8px', border: '1px solid #ddd', fontSize: '14px' }}
            />
            <button onClick={() => setCount(c => c + 1)}
              style={{ padding: '10px 16px', background: '#888', color: '#fff', border: 'none', borderRadius: '8px' }}>
              Рендер ({count})
            </button>
          </div>
          <p style={{ color: '#888', fontSize: '13px' }}>
            Найдено: <strong>{filtered.length}</strong> из {ITEMS.length}
            {' · '}Нажми "Рендер" — фильтрация не пересчитывается (useMemo)
          </p>
          <div style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #eee', borderRadius: '8px' }}>
            {filtered.slice(0, 50).map((item, i) => (
              <div key={i} style={{ padding: '8px 16px', borderBottom: '1px solid #f5f5f5', fontSize: '14px' }}>{item}</div>
            ))}
          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<SearchList />);"""),
        "solution": wrap("""    const ITEMS = Array.from({length:1000},(_,i)=>`Item ${i+1}`);
    function App() {
      const [q, setQ] = React.useState('');
      const filtered = React.useMemo(() => ITEMS.filter(i => i.includes(q)), [q]);
      return (
        <div>
          <input value={q} onChange={e => setQ(e.target.value)} placeholder="Поиск..." />
          <p>Найдено: {filtered.length}</p>
          {filtered.slice(0,20).map((i,idx) => <div key={idx}>{i}</div>)}
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "useMemo(fn, [deps]) — кэширует результат fn, пересчитывает только при изменении deps",
            "Кнопка 'Рендер' вызывает рендер но useMemo не пересчитывает — query не изменился",
            "Не злоупотребляй useMemo — используй только для действительно тяжёлых вычислений"
        ]),
    },
    {
        "title": "Error Boundary — обработка ошибок",
        "order": 7, "xp_reward": 35,
        "content": """## Что такое Error Boundary?

Если компонент выбрасывает ошибку — React размонтирует всё дерево. Error Boundary перехватывает ошибку и показывает fallback UI.

**Важно:** Error Boundary — только классовый компонент (для этого функциональные не подходят):

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("Ошибка:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return <div>Что-то пошло не так: {this.state.error.message}</div>;
    }
    return this.props.children;
  }
}
```

## Использование

```jsx
<ErrorBoundary>
  <ComponentThatMightFail />
</ErrorBoundary>
```

## Задание

Нажми кнопку — компонент сломается. Error Boundary перехватит ошибку и покажет красивый fallback.
""",
        "starter_code": wrap("""    class ErrorBoundary extends React.Component {
      constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
      }

      static getDerivedStateFromError(error) {
        return { hasError: true, error };
      }

      componentDidCatch(error, info) {
        console.error('Error Boundary поймал:', error.message);
      }

      render() {
        if (this.state.hasError) {
          return (
            <div style={{ padding: '24px', background: '#fff5f5', border: '1px solid #feb2b2', borderRadius: '12px' }}>
              <div style={{ fontSize: '32px', marginBottom: '12px' }}>💥</div>
              <h3 style={{ color: '#e53e3e', margin: '0 0 8px' }}>Что-то пошло не так</h3>
              <p style={{ color: '#666', fontSize: '14px', marginBottom: '16px' }}>
                {this.state.error.message}
              </p>
              <button
                onClick={() => this.setState({ hasError: false, error: null })}
                style={{ padding: '8px 20px', background: '#e53e3e', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
              >
                Попробовать снова
              </button>
            </div>
          );
        }
        return this.props.children;
      }
    }

    function BrokenComponent({ shouldBreak }) {
      if (shouldBreak) {
        throw new Error('Намеренная ошибка в компоненте!');
      }
      return (
        <div style={{ padding: '20px', background: '#f0fffe', border: '1px solid #9decf9', borderRadius: '12px' }}>
          <div style={{ fontSize: '32px' }}>✅</div>
          <p>Компонент работает нормально</p>
        </div>
      );
    }

    function App() {
      const [broken, setBroken] = React.useState(false);

      return (
        <div style={{ padding: '24px', maxWidth: '480px' }}>
          <h2>Error Boundary демо</h2>
          <button
            onClick={() => setBroken(b => !b)}
            style={{ marginBottom: '20px', padding: '10px 24px', background: broken ? '#27ae60' : '#e53e3e', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
          >
            {broken ? 'Починить компонент' : 'Сломать компонент'}
          </button>

          <ErrorBoundary key={broken}>
            <BrokenComponent shouldBreak={broken} />
          </ErrorBoundary>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    class EB extends React.Component {
      state = { err: null };
      static getDerivedStateFromError(e) { return { err: e }; }
      render() {
        if (this.state.err) return <div style={{color:'red'}}>Ошибка: {this.state.err.message}</div>;
        return this.props.children;
      }
    }
    function Bad({ fail }) {
      if (fail) throw new Error('Упс!');
      return <div>OK</div>;
    }
    function App() {
      const [fail, setFail] = React.useState(false);
      return <div><button onClick={() => setFail(f=>!f)}>Toggle</button><EB key={fail}><Bad fail={fail} /></EB></div>;
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "getDerivedStateFromError — статический метод, вызывается при ошибке потомка",
            "componentDidCatch — для логирования ошибок (например в Sentry)",
            "key={broken} на ErrorBoundary — сбрасывает его состояние при изменении"
        ]),
    },
    {
        "title": "Финальный проект: GitHub профиль",
        "order": 8, "xp_reward": 60,
        "content": """## Финальный проект курса

Создай приложение для просмотра GitHub-профилей с использованием GitHub API.

## Что использовать:
- `useState` — данные пользователя, ввод, ошибки, загрузка
- `useEffect` — запрос к API при изменении username
- `useCallback` — стабильная функция загрузки
- `useMemo` — вычисление статистики
- Error Boundary — обработка ошибок

## API эндпоинты:
```
GET https://api.github.com/users/{username}
GET https://api.github.com/users/{username}/repos?sort=stars&per_page=5
```

## Задание

Введи имя GitHub пользователя (например `torvalds`, `gvanrossum`) и посмотри его профиль.
""",
        "starter_code": wrap("""    class ErrorBoundary extends React.Component {
      state = { err: null };
      static getDerivedStateFromError(e) { return { err: e }; }
      render() {
        if (this.state.err) return <div style={{color:'red',padding:'20px'}}>❌ {this.state.err.message}</div>;
        return this.props.children;
      }
    }

    function GitHubProfile() {
      const [username, setUsername] = React.useState('torvalds');
      const [input, setInput] = React.useState('torvalds');
      const [user, setUser] = React.useState(null);
      const [repos, setRepos] = React.useState([]);
      const [loading, setLoading] = React.useState(false);
      const [error, setError] = React.useState(null);

      const loadUser = React.useCallback(async (name) => {
        setLoading(true);
        setError(null);
        try {
          const [uRes, rRes] = await Promise.all([
            fetch(`https://api.github.com/users/${name}`),
            fetch(`https://api.github.com/users/${name}/repos?sort=stars&per_page=5`)
          ]);
          if (!uRes.ok) throw new Error(`Пользователь "${name}" не найден`);
          const [userData, reposData] = await Promise.all([uRes.json(), rRes.json()]);
          setUser(userData);
          setRepos(reposData);
        } catch (e) {
          setError(e.message);
          setUser(null);
        } finally {
          setLoading(false);
        }
      }, []);

      React.useEffect(() => { loadUser(username); }, [username, loadUser]);

      const totalStars = React.useMemo(
        () => repos.reduce((s, r) => s + r.stargazers_count, 0),
        [repos]
      );

      return (
        <div style={{ maxWidth: '520px', margin: '0 auto', padding: '20px', fontFamily: 'Arial' }}>
          <h2>🔍 GitHub Профиль</h2>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
            <input value={input} onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && setUsername(input)}
              placeholder="Имя пользователя..."
              style={{ flex: 1, padding: '10px 14px', borderRadius: '8px', border: '1px solid #ddd', fontSize: '14px' }} />
            <button onClick={() => setUsername(input)}
              style={{ padding: '10px 20px', background: '#24292e', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer' }}>
              Найти
            </button>
          </div>

          {loading && <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>⏳ Загрузка...</div>}
          {error && <div style={{ padding: '16px', background: '#fff5f5', borderRadius: '8px', color: '#e53e3e' }}>❌ {error}</div>}

          {user && !loading && (
            <>
              <div style={{ display: 'flex', gap: '16px', alignItems: 'center', background: '#f6f8fa', padding: '20px', borderRadius: '12px', marginBottom: '16px' }}>
                <img src={user.avatar_url} alt="avatar"
                  style={{ width: '72px', height: '72px', borderRadius: '50%', border: '3px solid #fff', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }} />
                <div>
                  <div style={{ fontWeight: '700', fontSize: '18px' }}>{user.name || user.login}</div>
                  <div style={{ color: '#888', fontSize: '13px' }}>@{user.login}</div>
                  {user.bio && <div style={{ fontSize: '13px', marginTop: '4px', color: '#555' }}>{user.bio}</div>}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
                {[
                  { label: 'Репозитории', value: user.public_repos },
                  { label: 'Подписчики', value: user.followers },
                  { label: 'Звёзды (топ-5)', value: totalStars },
                ].map(stat => (
                  <div key={stat.label} style={{ flex: 1, textAlign: 'center', padding: '12px', background: '#fff', border: '1px solid #eee', borderRadius: '8px' }}>
                    <div style={{ fontSize: '20px', fontWeight: '700' }}>{stat.value?.toLocaleString()}</div>
                    <div style={{ fontSize: '11px', color: '#888', marginTop: '2px' }}>{stat.label}</div>
                  </div>
                ))}
              </div>

              {repos.length > 0 && (
                <>
                  <h3 style={{ margin: '0 0 12px', fontSize: '15px' }}>⭐ Популярные репозитории</h3>
                  {repos.map(repo => (
                    <div key={repo.id} style={{ padding: '12px 16px', background: '#fff', border: '1px solid #eee', borderRadius: '8px', marginBottom: '8px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{ fontWeight: '600', fontSize: '14px', color: '#0366d6' }}>{repo.name}</span>
                        <span style={{ fontSize: '13px', color: '#888' }}>⭐ {repo.stargazers_count.toLocaleString()}</span>
                      </div>
                      {repo.description && <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>{repo.description}</div>}
                    </div>
                  ))}
                </>
              )}
            </>
          )}
        </div>
      );
    }

    function App() {
      return (
        <ErrorBoundary>
          <GitHubProfile />
        </ErrorBoundary>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "solution": wrap("""    function App() {
      const [user, setUser] = React.useState(null);
      const [q, setQ] = React.useState('torvalds');
      React.useEffect(() => {
        fetch(`https://api.github.com/users/${q}`).then(r=>r.json()).then(setUser);
      }, [q]);
      return (
        <div>
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="username" />
          {user && <div><img src={user.avatar_url} width={60} style={{borderRadius:'50%'}} /><p>{user.name}</p><p>Repos: {user.public_repos}</p></div>}
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);"""),
        "tests": "[]",
        "hints": json.dumps([
            "Promise.all([fetch1, fetch2]) — делает два запроса параллельно",
            "useMemo для totalStars — пересчитывается только при изменении repos",
            "useCallback с [] — функция создаётся один раз и не меняется"
        ]),
    },
]


async def seed():
    async with Session() as db:
        result = await db.execute(
            select(Course).where(Course.title == "React: продвинутый уровень")
        )
        if result.scalar_one_or_none():
            print("⚠️  Курс уже существует")
            return

        course = Course(
            title="React: продвинутый уровень",
            description="Порталы, Lazy loading, Error Boundary, Context+Reducer, паттерны компонентов, виртуализация и оптимизация. Финальный проект — GitHub профиль viewer.",
            language=LanguageEnum.javascript,
            level=LevelEnum.advanced,
            order=4,
            is_published=True,
        )
        db.add(course)
        await db.flush()

        for data in LESSONS:
            db.add(Lesson(course_id=course.id, **data))

        await db.commit()
        print(f"✅ Курс '{course.title}' добавлен — {len(LESSONS)} уроков")


if __name__ == "__main__":
    asyncio.run(seed())
