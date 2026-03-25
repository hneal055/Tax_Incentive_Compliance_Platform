import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Navbar from "../components/Navbar";

// ─── Mock the store ───────────────────────────────────────────────────────────

const mockMarkRead = vi.fn();

type StoreState = { unreadEventCount: number; markRead: () => void };

const storeState: StoreState = { unreadEventCount: 0, markRead: mockMarkRead };

vi.mock("../store", () => ({
  useAppStore: vi.fn((selector: (s: StoreState) => unknown) =>
    selector(storeState),
  ),
}));

const renderNavbar = () =>
  render(
    <BrowserRouter>
      <Navbar />
    </BrowserRouter>,
  );

// ─── Tests ───────────────────────────────────────────────────────────────────

describe("Navbar", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    storeState.unreadEventCount = 0;
  });

  it("renders brand name", () => {
    renderNavbar();
    expect(screen.getByText("PilotForge")).toBeInTheDocument();
  });

  it("renders navigation links", () => {
    renderNavbar();
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Productions")).toBeInTheDocument();
  });

  it("renders a notification bell button", () => {
    renderNavbar();
    const bell = screen.getByLabelText(/Notifications/i);
    expect(bell).toBeInTheDocument();
  });

  it("hides the badge when unreadCount is 0", () => {
    storeState.unreadEventCount = 0;
    renderNavbar();
    expect(screen.queryByTestId("notification-badge")).not.toBeInTheDocument();
  });

  it("shows badge with count when unreadCount > 0", () => {
    storeState.unreadEventCount = 5;
    renderNavbar();
    const badge = screen.getByTestId("notification-badge");
    expect(badge).toBeInTheDocument();
    expect(badge.textContent).toBe("5");
  });

  it('shows "9+" when unreadCount exceeds 9', () => {
    storeState.unreadEventCount = 15;
    renderNavbar();
    const badge = screen.getByTestId("notification-badge");
    expect(badge.textContent).toBe("9+");
  });

  it("calls markRead when the bell button is clicked", () => {
    storeState.unreadEventCount = 3;
    renderNavbar();
    const bell = screen.getByLabelText(/Notifications/i);
    fireEvent.click(bell);
    expect(mockMarkRead).toHaveBeenCalledOnce();
  });
});
